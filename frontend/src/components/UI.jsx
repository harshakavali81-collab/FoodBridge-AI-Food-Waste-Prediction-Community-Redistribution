import React from "react";
export function Label({children}){return <span className="eyebrow">{children}</span>}
export function Pill({children,tone="neutral"}){return <span className={"pill "+tone}>{children}</span>}
export function Head({label,title,description}){return <div className="head"><Label>{label}</Label><h2>{title}</h2>{description&&<p>{description}</p>}</div>}
export function Kpi({label,value,unit,icon}){return <div className="kpi"><div className="kpi-top"><span>{label}</span><span className="kpi-icon">{icon}</span></div><strong>{value}<small> {unit}</small></strong><span className="kpi-note">Demonstration workspace</span></div>}
export function Notice(){return <div className="notice"><strong>◈ Synthetic demonstration</strong><span>All sample partners are fictional. Food safety, identity and physical collection require authorized human verification.</span></div>}
export function Empty({children="No records yet."}){return <div className="empty">{children}</div>}
export function ErrorText({message}){return message?<p role="alert" className="error">{message}</p>:null}
