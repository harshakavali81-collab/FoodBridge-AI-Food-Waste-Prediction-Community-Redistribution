// This public demo deliberately never handles privileged server credentials.
// In a real multi-user app use an audited BFF, secure sessions, RBAC and CSRF protection.
const BASE=(import.meta.env.VITE_API_BASE_URL || "/api/v1").replace(/\/$/,"");
export async function request(path,options={}){
 const response=await fetch(BASE+path,{
  ...options,
  credentials:"same-origin",
  headers:{...(options.body?{"Content-Type":"application/json"}:{}),...options.headers}
 });
 if(!response.ok){let reason=response.statusText;try{const j=await response.json();reason=typeof j.detail==="string"?j.detail:JSON.stringify(j.detail)}catch{}throw new Error(reason||"Network error")}
 if(response.headers.get("content-type")?.includes("application/json"))return response.json();
 return response.text();
}
export const api={
 dashboard:()=>request("/dashboard"),trends:()=>request("/analytics/trends"),forecast:()=>request("/forecast/preview"),
 inventory:()=>request("/inventory"),recipients:()=>request("/recipients"),donations:()=>request("/donations"),
 matches:id=>request("/matches/"+id),
 createItem:data=>request("/inventory",{method:"POST",body:JSON.stringify(data)}),
 createRecipient:data=>request("/recipients",{method:"POST",body:JSON.stringify(data)}),
 reserve:data=>request("/donations",{method:"POST",body:JSON.stringify(data)}),
 confirm:(id,name)=>request("/donations/"+id+"/confirm",{method:"POST",body:JSON.stringify({confirmed_by:name})}),
 cancel:id=>request("/donations/"+id+"/cancel",{method:"POST"})
};
