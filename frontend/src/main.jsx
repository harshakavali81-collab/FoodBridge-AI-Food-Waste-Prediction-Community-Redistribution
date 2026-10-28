import React,{useEffect,useState,useCallback} from "react";
import {createRoot} from "react-dom/client";
import {RefreshCw,Menu,X} from "lucide-react";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Surplus from "./pages/Surplus";
import RecipientMatches from "./pages/RecipientMatches";
import Donations from "./pages/Donations";
import Recipients from "./pages/Recipients";
import Analytics from "./pages/Analytics";
import {Notice,ErrorText} from "./components/UI";
import {api} from "./api/client";
import "./style.css";
function App(){
 const [page,setPage]=useState("dashboard"),[mobile,setMobile]=useState(false),[data,setData]=useState({}),[loading,setLoading]=useState(true),[error,setError]=useState("");
 const go=(page)=>{setPage(page);setMobile(false);window.scrollTo(0,0)};
 const refresh=useCallback(async()=>{try{const [stats,trends,inventory,recipients,donations,forecast]=await Promise.all([api.dashboard(),api.trends(),api.inventory(),api.recipients(),api.donations(),api.forecast()]);setData({stats,trends,inventory,recipients,donations,forecast});setError("")}catch(e){setError(e.message)}finally{setLoading(false)}},[]);
 useEffect(()=>{refresh()},[refresh]);
 const pages={dashboard:<Dashboard {...data} onNavigate={go}/>,surplus:<Surplus items={data.inventory||[]} refresh={refresh} onNavigate={go}/>,matches:<RecipientMatches items={data.inventory||[]} refresh={refresh} onNavigate={go}/>,donations:<Donations items={data.inventory||[]} recipients={data.recipients||[]} donations={data.donations||[]} refresh={refresh}/>,recipients:<Recipients recipients={data.recipients||[]}/>,analytics:<Analytics trends={data.trends} forecast={data.forecast}/>};
 return <div className="shell"><div className={"sidebar-wrap "+(mobile?"show":"")}><Sidebar page={page} onNavigate={go}/></div>{mobile&&<div className="backdrop" onClick={()=>setMobile(false)}/>}<main className="main"><header className="topbar"><div className="crumb"><button className="mobile-toggle" onClick={()=>setMobile(!mobile)}>{mobile?<X size={21}/>:<Menu size={21}/>}</button>Workspace <span>/</span> <strong>{page.charAt(0).toUpperCase()+page.slice(1)}</strong></div><div className="right"><button aria-label="Refresh dashboard" className="icon-btn" onClick={refresh}><RefreshCw size={18}/></button><div className="avatar">FB</div><div><b>FoodBridge Demo</b><small>Education workspace</small></div></div></header><div className="container"><div className="greeting"><div><span className="eyebrow">THE COMMUNITY FOOD INTELLIGENCE HUB</span><h1>{page==="dashboard"?"Good food. Good impact. 🌿":{surplus:"Manage your surplus",matches:"Find suitable recipients",donations:"From reservation to pickup",recipients:"Community partners",analytics:"Explore the numbers"}[page]}</h1><p>Make informed decisions, with people responsible for safety.</p></div><span className="date-chip">{new Date().toLocaleDateString("en-IN",{day:"numeric",month:"short",year:"numeric"})}</span></div><Notice/><ErrorText message={error}/>{loading?<div className="panel">Loading demonstration data...</div>:pages[page]}<footer>© 2026 FoodBridge AI · Synthetic-data educational project · Human-in-the-loop food safety</footer></div></main></div>
}
createRoot(document.getElementById("root")).render(<App/>);
