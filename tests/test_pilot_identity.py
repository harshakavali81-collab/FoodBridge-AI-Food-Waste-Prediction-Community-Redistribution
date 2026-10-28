"""JWT, roles, tenant isolation, simulated approvals and real-operation denial."""
from datetime import datetime,timedelta,timezone

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from backend.app.routes.pilot import CHECKS

ROOT="/api/v1"
@pytest.fixture()
def sign_token(monkeypatch):
    private=rsa.generate_private_key(public_exponent=65537,key_size=2048)
    public=private.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    monkeypatch.setenv("OIDC_PUBLIC_KEY_PEM",public)
    monkeypatch.setenv("OIDC_ISSUER","https://identity.example.test")
    monkeypatch.setenv("OIDC_AUDIENCE","foodbridge-internal")
    def make(sub="alice",tenant="org_alpha",roles=None,**overrides):
        now=datetime.now(timezone.utc)
        claims={"sub":sub,"tenant_id":tenant,"roles":roles or ["reviewer"],
                "iss":"https://identity.example.test",
                "aud":"foodbridge-internal","iat":now,"exp":now+timedelta(minutes=20)}
        claims.update(overrides)
        return jwt.encode(claims,private,algorithm="RS256")
    return make

def headers(token,**extra):
    return {"Authorization":"Bearer "+token,**extra}

def test_requires_signed_bearer_and_explicit_config(client,sign_token,monkeypatch):
    assert client.get(ROOT+"/identity/me").status_code==401
    good=sign_token(sub="user1",tenant="t_123",roles=["auditor","operator"])
    result=client.get(ROOT+"/identity/me",headers=headers(good))
    assert result.status_code==200,result.text
    assert result.json()["tenant_id"]=="t_123"
    assert result.json()["real_food_operations_authorized"] is False
    assert client.get(ROOT+"/identity/me",headers=headers(good+"tamper")).status_code==401
    monkeypatch.delenv("OIDC_PUBLIC_KEY_PEM")
    assert client.get(ROOT+"/identity/me",headers=headers(good)).status_code==503

@pytest.mark.parametrize("claim_patch,expected",[
    ({"aud":"different-audience"},401),
    ({"iss":"https://wrong.example.test"},401),
    ({"exp":datetime.now(timezone.utc)-timedelta(hours=1)},401),
    ({"roles":["godmode"]},403),
    ({"tenant_id":"../escape"},403),
    ({"roles":"admin"},403),
    ({"sub":"a"},403),
])
def test_rejects_bad_tokens(client,sign_token,claim_patch,expected):
    signed=sign_token(**claim_patch)
    assert client.get(ROOT+"/identity/me",headers=headers(signed)).status_code==expected

def test_role_checks_and_tenant_scope(client,sign_token):
    t1=sign_token(sub="reviewerA",tenant="tenant_one",roles=["reviewer"])
    t2=sign_token(sub="reviewerB",tenant="tenant_two",roles=["reviewer"])
    auditor=sign_token(sub="auditorX",tenant="tenant_one",roles=["auditor"])
    a=client.post(ROOT+"/pilot/reviews",headers=headers(t1),json={
        "check_key":"donor_identity","status":"accepted_demo","evidence_ref":"demo:donor-check"
    })
    assert a.status_code==201,a.text
    b=client.get(ROOT+"/pilot/readiness",headers=headers(t2))
    assert b.status_code==200
    assert b.json()["checks"]["donor_identity"]["status"]=="missing"
    b=client.get(ROOT+"/pilot/readiness",headers=headers(t1))
    assert b.json()["checks"]["donor_identity"]["status"]=="accepted_demo"
    assert client.post(ROOT+"/pilot/reviews",headers=headers(auditor),json={
        "check_key":"donor_identity","status":"accepted_demo","evidence_ref":"demo:staff-check"
    }).status_code==403
    assert client.post(ROOT+"/pilot/evaluate",headers=headers(t1)).status_code==403

def test_evidence_requires_mock_reference(client,sign_token):
    tok=sign_token()
    payload={"check_key":"donor_identity","status":"accepted_demo","evidence_ref":"https://real-private-record.example/"}
    assert client.post(ROOT+"/pilot/reviews",headers=headers(tok),json=payload).status_code==422
    payload["check_key"]="made_up"
    payload["evidence_ref"]="demo:mock-reference"
    assert client.post(ROOT+"/pilot/reviews",headers=headers(tok),json=payload).status_code==422

def test_requires_two_distinct_reviewers_and_all_eight_checks(client,sign_token):
    primary=sign_token(sub="primaryReviewer",tenant="tenant_three",roles=["reviewer"])
    secondary=sign_token(sub="secondReviewer",tenant="tenant_three",roles=["reviewer"])
    admin=sign_token(sub="adminOne",tenant="tenant_three",roles=["admin"])
    before=client.post(ROOT+"/pilot/evaluate",headers=headers(admin))
    assert before.status_code==200
    assert before.json()["simulation_outcome"]=="blocked"
    for key in CHECKS:
        resp=client.post(ROOT+"/pilot/reviews",headers=headers(primary),json={
            "check_key":key,"status":"accepted_demo","evidence_ref":f"demo:{key}"
        })
        assert resp.status_code==201,resp.text
    one=client.post(ROOT+"/pilot/evaluate",headers=headers(admin)).json()
    assert one["simulation_outcome"]=="blocked"
    assert not one["minimum_two_reviewers_met"]
    overwrite=client.post(ROOT+"/pilot/reviews",headers=headers(secondary),json={
        "check_key":"safe_handling_plan","status":"accepted_demo","evidence_ref":"demo:mock-food-safety-check"
    })
    assert overwrite.status_code==201
    result=client.post(ROOT+"/pilot/evaluate",headers=headers(admin)).json()
    assert result["simulation_outcome"]=="demo_ready"
    assert result["authorized_for_real_distribution"] is False
    assert client.get(ROOT+"/pilot/readiness",headers=headers(admin)).json()["distinct_reviewers"]==2

def test_rejects_pending_or_negative_review(client,sign_token):
    reviewer=sign_token(tenant="tenant_revoked")
    admin=sign_token(sub="pilotAdmin",tenant="tenant_revoked",roles=["admin"])
    client.post(ROOT+"/pilot/reviews",headers=headers(reviewer),json={
        "check_key":"donor_identity","status":"rejected_demo","evidence_ref":"demo:failed-review"
    })
    decision=client.post(ROOT+"/pilot/evaluate",headers=headers(admin)).json()
    assert "donor_identity" in decision["missing_checks"]
    assert decision["simulation_outcome"]=="blocked"

def test_production_pilot_writes_always_denied(client,sign_token,monkeypatch):
    token=sign_token()
    monkeypatch.setenv("APP_ENV","production")
    monkeypatch.setenv("API_KEY","Z"*44)
    extra={"X-API-Key":"Z"*44}
    submission=client.post(ROOT+"/pilot/reviews",headers=headers(token,**extra),json={
        "check_key":"donor_identity","status":"accepted_demo","evidence_ref":"demo:fake-record"
    })
    assert submission.status_code==403
    assert client.post(ROOT+"/pilot/evaluate",headers=headers(token,**extra)).status_code==403
