// ==========================
// CONFIG
// ==========================
const API_URL = "https://newdayai-production.up.railway.app";
const API_URL = "https://SENIN_RENDER_DOMAININ.onrender.com"; // Render URL

// ==========================
// GERÇEK FORM API
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
    const res = await fetch(`${API_URL}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ home, away })
    });

    const data = await res.json();

    document.getElementById("homeFormText").textContent =
      `${data.home} Son 5 Maç: ${data.form_home || "-"}`;

    document.getElementById("awayFormText").textContent =
      `${data.away} Son 5 Maç: ${data.form_away || "-"}`;

    const hp = Math.round(data.prediction.home_prob * 100);
    const dp = Math.round(data.prediction.draw_prob * 100);
    const ap = Math.round(data.prediction.away_prob * 100);

    homeProbLabel.textContent = data.home;
    awayProbLabel.textContent = data.away;

    homeProbEl.textContent = `${hp}%`;
    drawProbEl.textContent = `${dp}%`;
    awayProbEl.textContent = `${ap}%`;

    resultTitle.textContent = `${data.home} – ${data.away} Tahmini`;

    resultCard.classList.remove("hidden");
  });
});

async function fetchForm(team) {
  try {
    const res = await fetch(`${API_URL}/form/${encodeURIComponent(team)}`);
    const data = await res.json();

    if (data.error) {
      return { formString: "", matches: [], logoUrl: null, teamName: team };
    }

    return {
      formString: data.form || data.form_string || "",
      matches: data.matches || [],
      logoUrl: data.logoUrl || data.logo_url || data.logo || null,
      teamName: data.team || data.team_name || team
    };

  } catch (err) {
    console.error("fetchForm ERROR:", err);
    return { formString: "", matches: [], logoUrl: null, teamName: team };
  }
}

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
    const homeForm = await fetchForm(home);
    const awayForm = await fetchForm(away);

    document.getElementById("homeFormText").textContent =
      `${homeForm.teamName} Son 5 Maç: ${homeForm.formString}`;

    document.getElementById("awayFormText").textContent =
      `${awayForm.teamName} Son 5 Maç: ${awayForm.formString}`;

    // LOGOLAR
    if (homeForm.logoUrl) {
      homeLogoEl.src = homeForm.logoUrl;
      homeLogoEl.classList.remove("hidden");
    } else {
      homeLogoEl.classList.add("hidden");
    }

    if (awayForm.logoUrl) {
      awayLogoEl.src = awayForm.logoUrl;
      awayLogoEl.classList.remove("hidden");
    } else {
      awayLogoEl.classList.add("hidden");
    }

    // Şimdilik fake tahmin (backend model hazır olana kadar)
    generateFakeProbabilities(homeForm.teamName, awayForm.teamName);

    // 0.4 saniye sonra sonuç kartını göster
    setTimeout(() => {
      resultCard.classList.remove("hidden");
    }, 400);
  });
});

// ==========================
// ARKA PLAN RENKLERİ
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

function setBackgroundColors(home, away) {
  const h = TEAM_COLORS[normalizeKey(home)] || randomGradient();
  const a = TEAM_COLORS[normalizeKey(away)] || randomGradient(true);

  bgLeft.style.background = `linear-gradient(140deg, ${h[0]}, ${h[1]})`;
  bgRight.style.background = `linear-gradient(220deg, ${a[0]}, ${a[1]})`;
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
  } catch (err) {
    console.error("vsSound error:", err);
  }
}

// ==========================
// LOADING STEPLER
// ==========================
function runLoadingSteps(onComplete) {
  loadingSteps.classList.remove("hidden");
  resultCard.classList.add("hidden");

  const items = Array.from(loadingSteps.querySelectorAll("li"));
  items.forEach(li => li.classList.remove("processing", "done"));

  let idx = 0;

  function next() {
    if (idx > 0) {
      items[idx - 1].classList.remove("processing");
      items[idx - 1].classList.add("done");
    }

    if (idx >= items.length) {
      if (typeof onComplete === "function") {
        setTimeout(() => {
          onComplete();
        }, 400);
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
// SAHTE YÜZDELER (ŞİMDİLİK)
// ==========================
function generateFakeProbabilities(home, away) {
  let h = 40 + Math.random() * 20;
  let a = 20 + Math.random() * 25;
  let d = 100 - (h + a);

  h = Math.round(h);
  a = Math.round(a);
  d = Math.max(0, Math.round(d));

  homeProbLabel.textContent = home;
  awayProbLabel.textContent = away;

  homeProbEl.textContent = `${h}%`;
  awayProbEl.textContent = `${a}%`;
  drawProbEl.textContent = `${d}%`;

  resultTitle.textContent = `${home} – ${away} Tahmini`;
}

// ==========================
// TICKER (RASTGELE MAÇ TAHMİNİ)
// ==========================
async function loadTickerOnce() {
  try {
    const res = await fetch(`${API_URL}/fixtures/random`);
    const data = await res.json();

    if (data.error) {
      tickerContent.textContent = "Bugün için maç tahmini alınamadı.";
      return;
    }

    const { home, away, tournament, homeProb, awayProb, drawProb } = data;

    tickerContent.textContent =
      `${tournament} | ${home} ${homeProb}%  -  ${drawProb}% Beraberlik  -  ${awayProb}% ${away}`;
  } catch (err) {
    console.error("Ticker error:", err);
    tickerContent.textContent = "NewDay AI: Tahmin yüklenemedi.";
  }
}

function startTickerLoop() {
  loadTickerOnce();
  setInterval(loadTickerOnce, 25000); // 25 sn'de bir yeni maç
}

startTickerLoop();
