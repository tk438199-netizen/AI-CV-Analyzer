const API_URL = "https://ai-cv-analyzer-6o0.onrender.com";
const $ = (id) => document.getElementById(id);
const token = () => localStorage.getItem("cv_access_token");
const userSaved = () => { try { return JSON.parse(localStorage.getItem("cv_user") || "null"); } catch { return null; } };
const authHeaders = () => token() ? { Authorization: `Bearer ${token()}` } : {};

async function api(path, options = {}) {
  const headers = { ...(options.headers || {}), ...authHeaders() };
  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  let data = {}; try { data = await response.json(); } catch {}
  if (response.status === 401) {
    localStorage.removeItem("cv_access_token"); localStorage.removeItem("cv_user");
    if (!location.pathname.endsWith("login.html") && !location.pathname.endsWith("register.html")) location.href = "login.html";
  }
  if (!response.ok) throw new Error(data.detail || "Something went wrong.");
  return data;
}
function showMessage(el, msg, type = "error") { if (!el) return; el.textContent = msg; el.className = `message ${type}`; }
function setSession(data) {
  localStorage.setItem("cv_access_token", data.access_token);
  localStorage.setItem("cv_user", JSON.stringify(data.user));
}
function protectPage() {
  const protectedPage = document.body.classList.contains("app-page");
  if (protectedPage && !token()) { location.replace("login.html"); return false; }
  if ((location.pathname.endsWith("login.html") || location.pathname.endsWith("register.html")) && token()) {
    location.replace("dashboard.html"); return false;
  }
  return true;
}
if (protectPage()) {
  const registerForm = $("registerForm");
  if (registerForm) registerForm.addEventListener("submit", async e => {
    e.preventDefault();
    const msg = $("registerMessage"), btn = registerForm.querySelector("button");
    const password = $("password").value;
    if (password !== $("confirm_password").value) return showMessage(msg, "Passwords do not match.");
    btn.disabled = true; btn.textContent = "Creating account…";
    try {
      const data = await api("/auth/register", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({full_name:$("full_name").value.trim(), email:$("email").value.trim(), password}) });
      setSession(data); location.href = "dashboard.html";
    } catch(err) { showMessage(msg, err.message); }
    finally { btn.disabled = false; btn.textContent = "Create account →"; }
  });

  const loginForm = $("loginForm");
  if (loginForm) loginForm.addEventListener("submit", async e => {
    e.preventDefault(); const msg=$("loginMessage"), btn=loginForm.querySelector("button");
    btn.disabled=true; btn.textContent="Signing in…";
    try {
      const data=await api("/auth/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:$("email").value.trim(),password:$("password").value})});
      setSession(data); location.href="dashboard.html";
    } catch(err) { showMessage(msg,err.message); }
    finally { btn.disabled=false; btn.textContent="Sign in →"; }
  });

  if ($("logoutBtn")) $("logoutBtn").addEventListener("click",()=>{localStorage.removeItem("cv_access_token");localStorage.removeItem("cv_user");location.href="login.html";});

  async function loadProfile() {
    if (!$("userName")) return;
    try {
      const data=await api("/auth/me"), u=data.user;
      localStorage.setItem("cv_user",JSON.stringify(u));
      $("userName").textContent=u.full_name; $("userEmail").textContent=u.email;
      $("userAvatar").textContent=(u.full_name||"U").charAt(0).toUpperCase();
    } catch { const u=userSaved(); if(u){$("userName").textContent=u.full_name;$("userEmail").textContent=u.email;} }
  }

  async function loadHistory() {
    if (!$("historyList")) return;
    const list=$("historyList");
    try {
      const data=await api("/cv/history"), rows=data.history||[];
      $("totalAnalyses").textContent=data.total_records??rows.length;
      $("savedReports").textContent=rows.length;
      $("latestScore").textContent=rows.length && rows[0].predicted_score!=null ? `${Math.round(rows[0].predicted_score)}/100` : "—";
      if(!rows.length){list.innerHTML='<div class="history-empty"><span>◷</span><b>No reports yet</b><p>Your completed CV analyses will appear here.</p></div>';return;}
      list.innerHTML=rows.map(row=>`<button class="history-row" data-id="${row.id}"><span class="history-file">PDF</span><span class="history-meta"><b>${escapeHTML(row.filename)}</b><small>${formatDate(row.created_at)} · ${row.page_count??"—"} pages · ${row.word_count??"—"} words</small></span><strong>${row.predicted_score==null?"—":Math.round(row.predicted_score)+"/100"}</strong><span class="history-open">View report →</span></button>`).join("");
      list.querySelectorAll("[data-id]").forEach(btn=>btn.addEventListener("click",()=>openHistory(btn.dataset.id)));
    } catch(err) { list.innerHTML=`<div class="history-empty">${escapeHTML(err.message)}</div>`; }
  }
  async function openHistory(id) {
    try { const data=await api(`/cv/history/${id}`); localStorage.setItem("cv_current_result",JSON.stringify(data.analysis)); location.href="result.html"; }
    catch(err){alert(err.message);}
  }
  if($("refreshHistory")) $("refreshHistory").addEventListener("click",loadHistory);
  if($("historyList")) { loadProfile(); loadHistory(); }

  const uploadBtn=$("uploadBtn"), input=$("cvFile");
  if(uploadBtn && input) {
    uploadBtn.addEventListener("click",()=>input.click());
    const dz=$("dropzone");
    ["dragenter","dragover"].forEach(ev=>dz.addEventListener(ev,e=>{e.preventDefault();dz.classList.add("dragging");}));
    ["dragleave","drop"].forEach(ev=>dz.addEventListener(ev,e=>{e.preventDefault();dz.classList.remove("dragging");}));
    dz.addEventListener("drop",e=>{if(e.dataTransfer.files.length){input.files=e.dataTransfer.files;input.dispatchEvent(new Event("change"));}});
    input.addEventListener("change",async()=>{
      const file=input.files[0];if(!file)return;
      if(!file.name.toLowerCase().endsWith(".pdf"))return showMessage($("uploadMessage"),"Please choose a PDF file.");
      if(file.size>5*1024*1024)return showMessage($("uploadMessage"),"The file must be smaller than 5 MB.");
      $("selectedFile").textContent=file.name; uploadBtn.disabled=true;uploadBtn.textContent="Analyzing…";
      showMessage($("uploadMessage"),"Uploading and analyzing your CV. Please wait…","info");
      $("uploadProgress").classList.add("visible");$("progressBar").style.width="35%";
      try{
        const form=new FormData();form.append("file",file);
        const data=await api("/cv/analyze-complete",{method:"POST",body:form});
        $("progressBar").style.width="100%";localStorage.setItem("cv_current_result",JSON.stringify(data));
        showMessage($("uploadMessage"),"Analysis complete. Opening your report…","success");
        setTimeout(()=>location.href="result.html",450);
      }catch(err){showMessage($("uploadMessage"),err.message);}
      finally{uploadBtn.disabled=false;uploadBtn.textContent="Choose PDF file";}
    });
  }

  if($("cvScore")) {
    let result=null;
    try { result=JSON.parse(localStorage.getItem("cv_current_result")||"null"); } catch {}
    if(!result){location.replace("dashboard.html");}
    else renderResult(result);
  }
}
function escapeHTML(v){return String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
function formatDate(v){if(!v)return "Date unavailable";const d=new Date(v);return isNaN(d)?"Date unavailable":d.toLocaleString(undefined,{dateStyle:"medium",timeStyle:"short"});}
function flatten(value){
  if(value==null)return [];
  if(Array.isArray(value))return value.flatMap(flatten);
  if(typeof value==="object")return Object.entries(value).flatMap(([k,v])=>[`${k.replaceAll("_"," ")}: ${Array.isArray(v)?v.join(", "):typeof v==="object"?JSON.stringify(v):v}`]);
  return [String(value)];
}
function renderResult(r){
  const score=r.score_analysis?.predicted_score;
  $("cvScore").innerHTML=`${score==null?"—":Math.round(score)}<small>/100</small>`;
  $("reportFile").textContent=`${r.filename||"CV report"} · Analysis #${r.analysis_id??"saved"}`;
  $("pageCount").textContent=r.file_information?.page_count??"—";
  $("wordCount").textContent=r.file_information?.word_count??"—";
  $("skillsCount").textContent=r.skills_analysis?.total_skills??"—";
  $("projectsCount").textContent=r.projects_analysis?.total_projects??"—";
  const p=r.personal_information||{};
  $("personalInfo").innerHTML=Object.entries(p).filter(([,v])=>v).map(([k,v])=>`<p><small>${escapeHTML(k.replaceAll("_"," "))}</small><b>${escapeHTML(v)}</b></p>`).join("")||"<p>No personal information detected.</p>";
  $("educationInfo").innerHTML=flatten(r.education_analysis).map(v=>`<p>${escapeHTML(v)}</p>`).join("")||"<p>No education details detected.</p>";
  const skills=r.skills_analysis?.skills||{};
  $("skillsInfo").innerHTML=Object.values(skills).flat().map(v=>`<span>${escapeHTML(v)}</span>`).join("")||"<p>No skills detected.</p>";
  const projects=flatten(r.projects_analysis), exp=flatten(r.experience_analysis);
  $("projectsInfo").innerHTML=[...projects,...exp].map(v=>`<p>${escapeHTML(v)}</p>`).join("")||"<p>No project or experience details detected.</p>";
  let suggestions=r.improvement_analysis?.suggestions??r.improvement_analysis??[];
  if(!Array.isArray(suggestions))suggestions=flatten(suggestions);
  $("suggestionList").innerHTML=suggestions.length?suggestions.map((v,i)=>`<div class="suggestion"><b>${String(i+1).padStart(2,"0")}</b><span>${escapeHTML(typeof v==="string"?v:JSON.stringify(v))}</span></div>`).join(""):"<p>No suggestions available.</p>";
}