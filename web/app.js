// app.js

// ==========================
// CONFIG
// ==========================
const API_URL = "https://SENIN_RENDER_DOMAININ.onrender.com"; // Burayı kendi backend URL'inle değiştir

// ==========================
// ELEMENTLER
// ==========================
const homeInput = document.getElementById("homeTeam");
const awayInput = document.getElementById("awayTeam");
const analyzeBtn = document.getElementById("analyzeBtn");

const vsAnimation = document.getElementById("vsAnimation");
const vsHomeName = document.getElementById("vsHomeName");
const vsAwayName = document.getElementById("vsAwayName");
const vsSound = document.getElementById("vsSound");

const homeLogoEl = document.getElementById("homeLogo");
const awayLogoEl = document.getElementById("awayLogo");

const loadingSteps = document.getElementById("loadingSteps");
const resultCard = document.getElementById("resultCard");

const homeProbEl = document.getElementById("homeProb");
const awayProbEl = document.getElementById("awayProb");
const drawProbEl = document.getElementById("drawProb");

const homeProbLabel = document.getElementById("homeProbLabel");
const awayProbLabel = document.getElementById("awayProbLabel");

const resultTitle = document.getElementById("resultTitle");

const bgLeft = document.querySelector(".bg-left");
const bgRight = document.querySelector(".bg-right");

const tickerContent = document.getElementById("tickerContent");

document.getElementById("year").textContent = new Date().getFullYear();

// ==========================
// TAKIM RENKLERİ
// ==========================
const TEAM_COLORS = {
  galatasaray: ["#8C1A1A", "#F4C430"],
  fenerbahce: ["#002B7F", "#F6E11F"],
  trabzonspor: ["#7C0028", "#00A0B0"],
  besiktas: ["#111827", "#e5e7eb"],
  konyaspor: ["#006E3A", "#E5FFF2"],
};

function normalizeKey(name) {
  return name.toLowerCase().replace(/\s+/g, "");
}

function randomGradient(reverse) {
  const palettes = [
    ["#0EA5E9", "#1D4ED8"],
    ["#BE123C", "#F97316"],
    ["#16A34A", "#0F172A"],
    ["#7C3AED", "#22D3EE"],
    ["#F97316", "#FACC15"],
  ];
  const p = palettes[Math.floor(Math.random() * palettes.length)];
  return reverse ? p.reverse() : p;
}

function setBackgroundColors(home, away) {
  const h = TEAM_COLORS[normalizeKey(home)] || randomGradient();
  const a = TEAM_COLORS[normalizeKey(away)] || randomGradient(true);

  bgLeft.style.background = `linear-gradient(140deg, ${h[0]}, ${h[1]})`;
  bgRight.style.background = `linear-gradient(220deg, ${a[0]}, ${a[1]})`;
}

// ==========================
// VS ANİMASYON
// ==========================
function triggerVsAnimation() {
  vsAnimation.classList.remove("active");
  void vsAnimation.offsetWidth;
  vsAnimation.classList.add("active");

  try {
    vsSound.currentTime = 0;
    vsSound.play().catch(() => {});
  } catch {}
}

// ==========================
// LOADING STEPLER
// ==========================
function runLoadingSteps(onComplete) {
  loadingSteps.classList.remove("hidden");
  resultCard.classList.add("hidden");

  const items = Array.from(loadingSteps.querySelectorAll("li"));
  items.forEach((li) => li.classList.remove("processing", "done"));

  let idx = 0;

  function next() {
    if (idx > 0) {
      items[idx - 1].classList.remove("processing");
      items[idx - 1].classList.add("done");
    }

    if (idx >= items.length) {
      if (typeof onComplete === "function") {
        setTimeout(() => onComplete(), 400);
      }
      return;
    }

    items[idx].classList.add("processing");
    idx++;

    setTimeout(next, 400 + Math.random() * 250);
  }

  next();
}

// ==========================
// BACKEND ANALIZ
// ==========================
async function callAnalyzeAPI(home, away) {
  try {
    const res = await fetch(`${API_URL}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ home, away }),
    });

    if (!res.ok) {
      throw new Error("API response not ok");
    }

    return await res.json();
  } catch (err) {
    console.error("analyze API error:", err);
    throw err;
  }
}

// ==========================
// ANALİZ BUTONU
// ==========================
analyzeBtn.addEventListener("click", () => {
  const home = homeInput.value.trim();
  const away = awayInput.value.trim();

  if (!home || !away) {
    alert("İki takım adını da gir.");
    return;
  }

  setBackgroundColors(home, away);

  vsHomeName.textContent = home.toUpperCase();
  vsAwayName.textContent = away.toUpperCase();

  triggerVsAnimation();

  runLoadingSteps(async () => {
    try {
      const data = await callAnalyzeAPI(home, away);

      const formHome = data.form_home || "";
      const formAway = data.form_away || "";

      document.getElementById("homeFormText").textContent =
        `${data.home} Son 5 Maç: ${formHome || "-"}`;

      document.getElementById("awayFormText").textContent =
        `${data.away} Son 5 Maç: ${formAway || "-"}`;

      const hp = Math.round((data.prediction?.home_prob || 0) * 100);
      const dp = Math.round((data.prediction?.draw_prob || 0) * 100);
      const ap = Math.round((data.prediction?.away_prob || 0) * 100);

      homeProbLabel.textContent = data.home;
      awayProbLabel.textContent = data.away;

      homeProbEl.textContent = `${hp}%`;
      drawProbEl.textContent = `${dp}%`;
      awayProbEl.textContent = `${ap}%`;

      resultTitle.textContent = `${data.home} – ${data.away} Tahmini`;

      const homeLogo =
        data.raw?.home?.logo ||
        data.raw?.home?.team_logo ||
        null;
      const awayLogo =
        data.raw?.away?.logo ||
        data.raw?.away?.team_logo ||
        null;

      if (homeLogo) {
        homeLogoEl.src = homeLogo;
        homeLogoEl.classList.remove("hidden");
      } else {
        homeLogoEl.classList.add("hidden");
      }

      if (awayLogo) {
        awayLogoEl.src = awayLogo;
        awayLogoEl.classList.remove("hidden");
      } else {
        awayLogoEl.classList.add("hidden");
      }

      resultCard.classList.remove("hidden");
    } catch (err) {
      alert("Analiz sırasında bir hata oluştu. Daha sonra tekrar dene.");
      loadingSteps.classList.add("hidden");
    }
  });
});

// ==========================
// TICKER
// ==========================
async function loadTickerOnce() {
  try {
    const res = await fetch(`${API_URL}/fixtures/random`);
    if (!res.ok) throw new Error("ticker api not ok");
    const data = await res.json();

    if (data.error) {
      tickerContent.textContent = "Bugün için rastgele maç tahmini alınamadı.";
      return;
    }

    const home = data.home || "Ev";
    const away = data.away || "Dep";
    const tournament = data.tournament || "Lig";
    const hp = Math.round((data.homeProb || 0) * 100);
    const dp = Math.round((data.drawProb || 0) * 100);
    const ap = Math.round((data.awayProb || 0) * 100);

    tickerContent.textContent =
      `⚽ ${tournament} | ${home} ${hp}%  -  ${dp}% Beraberlik  -  ${ap}% ${away}`;
  } catch (err) {
    console.error("Ticker error:", err);
    tickerContent.textContent =
      "NewDay AI: Canlı bülten şu an yüklenemiyor.";
  }
}

function startTickerLoop() {
  loadTickerOnce();
  setInterval(loadTickerOnce, 25000);
}

startTickerLoop();
