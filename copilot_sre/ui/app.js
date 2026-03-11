const stateUrl = "/api/state";

const els = {
  severityBadge: document.getElementById("severityBadge"),
  topSuspect: document.getElementById("topSuspect"),
  incidentStart: document.getElementById("incidentStart"),
  incidentTitle: document.getElementById("incidentTitle"),
  incidentSummary: document.getElementById("incidentSummary"),
  symptoms: document.getElementById("symptoms"),
  actions: document.getElementById("actions"),
  suspects: document.getElementById("suspects"),
  mitigation: document.getElementById("mitigation"),
  rollback: document.getElementById("rollback"),
  timeline: document.getElementById("timeline"),
  commits: document.getElementById("commits"),
  pullRequests: document.getElementById("pullRequests"),
  runbooks: document.getElementById("runbooks"),
  alerts: document.getElementById("alerts"),
  dashboardMeta: document.getElementById("dashboardMeta"),
  dashboardSummary: document.getElementById("dashboardSummary"),
  dashboardNarrative: document.getElementById("dashboardNarrative"),
  kpiCards: document.getElementById("kpiCards"),
  metricExplorer: document.getElementById("metricExplorer"),
  latencyChart: document.getElementById("latencyChart"),
  errorChart: document.getElementById("errorChart"),
  conversionChart: document.getElementById("conversionChart"),
  promptBox: document.getElementById("promptBox"),
  copilotOutput: document.getElementById("copilotOutput"),
  statusBar: document.getElementById("statusBar"),
  demoPlayBtn: document.getElementById("demoPlayBtn"),
  demoReplayBtn: document.getElementById("demoReplayBtn"),
  demoStage: document.getElementById("demoStage"),
  demoTitle: document.getElementById("demoTitle"),
  demoBody: document.getElementById("demoBody"),
  demoStepLabel: document.getElementById("demoStepLabel"),
  demoProgressBar: document.getElementById("demoProgressBar"),
  demoProgressText: document.getElementById("demoProgressText"),
  demoModeText: document.getElementById("demoModeText"),
  githubRepo: document.getElementById("githubRepo"),
  githubLookback: document.getElementById("githubLookback"),
  azureAppId: document.getElementById("azureAppId"),
  azureLookback: document.getElementById("azureLookback"),
  githubBtn: document.getElementById("githubBtn"),
  azureBtn: document.getElementById("azureBtn"),
  copilotBtn: document.getElementById("copilotBtn"),
};

const demoTargets = new Map(
  Array.from(document.querySelectorAll(".demo-target")).map((node) => [node.dataset.demoId, node])
);

let demoTimeout = null;
let demoRunning = false;

const demoSteps = [
  {
    id: "controls",
    title: "Copilot SRE starts with context gathering",
    body: "We begin in the enrichment deck. This is where GitHub and Azure evidence can be pulled into the incident before any reasoning starts.",
  },
  {
    id: "suspects",
    title: "The system ranks likely root causes",
    body: "Instead of flooding the operator with raw signals, Copilot SRE turns the evidence into a prioritized suspect list with explainable scoring.",
  },
  {
    id: "timeline",
    title: "The incident timeline tells the operational story",
    body: "Deploys, alerts, and error logs are stitched into one narrative so the operator can see how the outage unfolded in seconds.",
  },
  {
    id: "context",
    title: "Live repository activity can be correlated",
    body: "GitHub commits, pull requests, and runbooks show what changed around the outage and which playbooks are relevant right now.",
    action: async () => {
      if (!els.githubRepo.value.trim()) {
        return;
      }
      await postJson(
        "/api/enrich/github",
        {
          repo: els.githubRepo.value,
          lookback_hours: Number(els.githubLookback.value || 24),
        },
        els.githubBtn,
        "Demo mode: correlating live GitHub activity..."
      );
    },
  },
  {
    id: "dashboards",
    title: "Azure insights become an interactive dashboard",
    body: "The dashboard turns telemetry into KPI cards, trend charts, and a short narrative that executives and operators can both understand at a glance.",
    action: async () => {
      if (!els.azureAppId.value.trim()) {
        return;
      }
      await postJson(
        "/api/enrich/azure",
        {
          app_id: els.azureAppId.value,
          lookback_minutes: Number(els.azureLookback.value || 30),
        },
        els.azureBtn,
        "Demo mode: loading rich Azure insights..."
      );
    },
  },
  {
    id: "telemetry",
    title: "The raw metric series stays visible",
    body: "Copilot SRE keeps the underlying metric points visible in the telemetry explorer so the dashboard remains explainable instead of magical.",
  },
  {
    id: "mitigation",
    title: "Mitigation options are operational, not generic",
    body: "The product suggests concrete next moves, with urgency and confidence, so an on-call engineer can act instead of translating chat output.",
  },
  {
    id: "rollback",
    title: "Rollback is treated as a decision, not a guess",
    body: "Copilot SRE explains whether rollback is warranted and how to verify recovery after the change is made.",
  },
  {
    id: "prompt",
    title: "Copilot receives a structured incident brief",
    body: "Once the operational picture is assembled, Copilot gets a high-signal handoff containing the incident summary, suspects, mitigation options, and verification plan.",
  },
  {
    id: "copilot",
    title: "The flow is ready for a live Copilot handoff",
    body: "If Copilot CLI is installed, the operator can run it from the UI. Even before that, the UI itself shows the full evidence-backed workflow end to end.",
  },
];

function setStatus(message, isError = false) {
  els.statusBar.textContent = message;
  els.statusBar.style.color = isError ? "#ffc4c4" : "#8aa5c7";
}

function clearDemoHighlight() {
  demoTargets.forEach((node) => node.classList.remove("active-demo-target"));
}

function updateDemoProgress(index) {
  const current = index + 1;
  els.demoProgressText.textContent = `${current} / ${demoSteps.length}`;
  els.demoProgressBar.style.width = `${(current / demoSteps.length) * 100}%`;
}

async function showDemoStep(index) {
  const step = demoSteps[index];
  if (!step) {
    clearDemoHighlight();
    els.demoTitle.textContent = "Guided demo complete";
    els.demoBody.textContent = "Replay it again or use the live controls to enrich, investigate, and hand the incident to Copilot.";
    els.demoStepLabel.textContent = "Completed";
    els.demoModeText.textContent = "Replay ready";
    els.demoPlayBtn.disabled = false;
    els.demoReplayBtn.disabled = false;
    demoRunning = false;
    return;
  }

  clearDemoHighlight();
  const target = demoTargets.get(step.id);
  if (target) {
    target.classList.add("active-demo-target");
    target.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  els.demoTitle.textContent = step.title;
  els.demoBody.textContent = step.body;
  els.demoStepLabel.textContent = `Step ${index + 1}`;
  els.demoModeText.textContent = "Autoplay";
  updateDemoProgress(index);

  if (step.action) {
    try {
      await step.action();
    } catch (error) {
      els.demoBody.textContent = `${step.body} Live enrichment failed: ${error.message}`;
    }
  }

  demoTimeout = window.setTimeout(() => {
    showDemoStep(index + 1);
  }, 3600);
}

function startDemo() {
  if (demoTimeout) {
    window.clearTimeout(demoTimeout);
  }
  demoRunning = true;
  els.demoPlayBtn.disabled = true;
  els.demoReplayBtn.disabled = true;
  els.demoModeText.textContent = "Autoplay";
  showDemoStep(0);
}

function list(container, items, render) {
  container.innerHTML = "";
  items.forEach((item) => container.appendChild(render(item)));
}

function li(text) {
  const item = document.createElement("li");
  item.textContent = text;
  return item;
}

function renderState(payload) {
  const { incident, analysis, mitigation, rollback, prompt, dashboard, app_insights_demo, source_app_insights_app_id } = payload;
  els.severityBadge.textContent = analysis.severity.toUpperCase();
  els.severityBadge.className = `severity-pill ${analysis.severity}`;
  els.topSuspect.textContent = analysis.suspects[0]?.title ?? "Unknown";
  els.incidentStart.textContent = incident.started_at;
  els.incidentTitle.textContent = `${incident.id} · ${incident.service}`;
  els.incidentSummary.textContent = analysis.summary;
  els.promptBox.textContent = prompt;

  list(els.symptoms, incident.symptoms, (text) => li(text));
  list(els.actions, analysis.recommended_actions, (text) => li(text));

  els.suspects.innerHTML = "";
  analysis.suspects.forEach((suspect) => {
    const card = document.createElement("div");
    card.className = "suspect";
    card.style.setProperty("--score", suspect.score);
    card.innerHTML = `
      <div class="suspect-head">
        <strong>${suspect.title}</strong>
        <span class="score-pill">Score ${suspect.score}</span>
      </div>
      <p>${suspect.rationale}</p>
    `;
    els.suspects.appendChild(card);
  });

  els.mitigation.innerHTML = "";
  mitigation.forEach((item) => {
    const card = document.createElement("div");
    card.className = "mitigation-item";
    card.innerHTML = `
      <div class="mitigation-head">
        <strong>${item.title}</strong>
        <span class="priority-pill ${item.priority.toLowerCase()}">${item.priority}</span>
      </div>
      <p>${item.rationale}</p>
      <small>Confidence: ${item.confidence}</small>
    `;
    els.mitigation.appendChild(card);
  });

  els.rollback.innerHTML = `
    <div class="rollback-box">
      <strong>${rollback.decision.toUpperCase()}</strong>
      <p>${rollback.rationale}</p>
      <small>Confidence: ${rollback.confidence}</small>
      <ul>${rollback.verification_steps.map((step) => `<li>${step}</li>`).join("")}</ul>
    </div>
  `;

  els.timeline.innerHTML = "";
  analysis.timeline.forEach((entry) => {
    const item = document.createElement("div");
    item.className = "timeline-item";
    const split = entry.split("  ");
    item.innerHTML = `<time>${split[0]}</time><p>${split.slice(1).join("  ")}</p>`;
    els.timeline.appendChild(item);
  });

  list(els.commits, incident.commits, (commit) => li(`${commit.sha} · ${commit.author} · ${commit.message}`));
  list(
    els.pullRequests,
    incident.pull_requests,
    (pr) => li(`#${pr.number} · ${pr.author} · ${pr.title} [${pr.state}]`)
  );
  list(els.runbooks, incident.runbooks, (runbook) => li(`${runbook.title} · ${runbook.summary}`));
  list(els.alerts, incident.alerts, (alert) => li(`${alert.name} · ${alert.severity} · ${alert.summary}`));
  renderDashboard(dashboard, incident.metrics, app_insights_demo, source_app_insights_app_id);
}

function renderDashboard(dashboard, metrics, isDemo, appId) {
  els.dashboardMeta.textContent = isDemo ? `Demo dataset · App ID ${appId}` : appId ? `Live App Insights · App ID ${appId}` : "Interactive telemetry story";
  els.dashboardSummary.textContent = dashboard?.headline || "Load the demo App Insights dataset to populate the telemetry dashboard.";

  els.kpiCards.innerHTML = "";
  (dashboard?.kpis || []).forEach((kpi) => {
    const card = document.createElement("div");
    card.className = `kpi-card ${kpi.tone || ""}`;
    card.innerHTML = `
      <span class="kpi-label">${kpi.label}</span>
      <span class="kpi-value">${kpi.value}</span>
      <span class="kpi-delta">${kpi.delta}</span>
    `;
    els.kpiCards.appendChild(card);
  });

  list(els.dashboardNarrative, dashboard?.narrative || [], (text) => li(text));

  const grouped = groupMetrics(metrics);
  drawMetricChart(els.latencyChart, grouped["appinsights.request_p95"] || grouped["checkout.p95_latency"] || [], "#74b9ff");
  drawMetricChart(els.errorChart, grouped["appinsights.failed_request_rate"] || grouped["checkout.http_5xx_rate"] || [], "#ff7d7d");
  drawMetricChart(els.conversionChart, grouped["appinsights.checkout_conversion_rate"] || grouped["checkout.conversion_rate"] || [], "#67f0c1");

  els.metricExplorer.innerHTML = "";
  metrics
    .slice()
    .sort((a, b) => a.timestamp.localeCompare(b.timestamp))
    .forEach((metric) => {
      const row = document.createElement("div");
      row.className = "metric-row";
      const pct = metric.baseline ? (((Number(metric.value) - Number(metric.baseline)) / Number(metric.baseline)) * 100).toFixed(0) : "0";
      row.innerHTML = `
        <span>${metric.name}</span>
        <span>${metric.timestamp}</span>
        <span>${metric.value}${metric.unit}</span>
        <span>${metric.baseline}${metric.unit}</span>
        <span>${pct}%</span>
      `;
      els.metricExplorer.appendChild(row);
    });
}

function groupMetrics(metrics) {
  return metrics.reduce((acc, metric) => {
    acc[metric.name] = acc[metric.name] || [];
    acc[metric.name].push(metric);
    return acc;
  }, {});
}

function drawMetricChart(svg, points, color) {
  svg.innerHTML = "";
  const width = 420;
  const height = 180;
  if (!points.length) {
    return;
  }

  const sorted = points.slice().sort((a, b) => a.timestamp.localeCompare(b.timestamp));
  const values = sorted.map((point) => Number(point.value));
  const max = Math.max(...values);
  const min = Math.min(...values);
  const range = max - min || 1;
  const pad = 20;

  const baseline = Number(sorted[sorted.length - 1].baseline || 0);
  if (baseline) {
    const y = height - pad - ((baseline - min) / range) * (height - pad * 2);
    const baselineLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
    baselineLine.setAttribute("x1", String(pad));
    baselineLine.setAttribute("x2", String(width - pad));
    baselineLine.setAttribute("y1", String(y));
    baselineLine.setAttribute("y2", String(y));
    baselineLine.setAttribute("stroke", "rgba(255,255,255,0.18)");
    baselineLine.setAttribute("stroke-dasharray", "4 4");
    svg.appendChild(baselineLine);
  }

  const coords = sorted.map((point, index) => {
    const x = pad + (index / Math.max(sorted.length - 1, 1)) * (width - pad * 2);
    const y = height - pad - ((Number(point.value) - min) / range) * (height - pad * 2);
    return [x, y];
  });

  const polyline = document.createElementNS("http://www.w3.org/2000/svg", "polyline");
  polyline.setAttribute("fill", "none");
  polyline.setAttribute("stroke", color);
  polyline.setAttribute("stroke-width", "4");
  polyline.setAttribute("points", coords.map(([x, y]) => `${x},${y}`).join(" "));
  svg.appendChild(polyline);

  coords.forEach(([x, y]) => {
    const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    dot.setAttribute("cx", String(x));
    dot.setAttribute("cy", String(y));
    dot.setAttribute("r", "4.5");
    dot.setAttribute("fill", color);
    svg.appendChild(dot);
  });
}

async function fetchState() {
  setStatus("Refreshing incident state...");
  const response = await fetch(stateUrl);
  const payload = await response.json();
  renderState(payload);
  setStatus("Ready.");
}

async function postJson(url, body, button, statusText) {
  button.disabled = true;
  setStatus(statusText);
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || "Request failed");
    }
    if (payload.analysis) {
      renderState(payload);
      setStatus("Incident state updated.");
    } else {
      return payload;
    }
  } catch (error) {
    setStatus(error.message, true);
    throw error;
  } finally {
    button.disabled = false;
  }
  return null;
}

els.githubBtn.addEventListener("click", async () => {
  await postJson(
    "/api/enrich/github",
    {
      repo: els.githubRepo.value,
      lookback_hours: Number(els.githubLookback.value || 24),
    },
    els.githubBtn,
    "Pulling live GitHub activity..."
  );
});

els.azureBtn.addEventListener("click", async () => {
  await postJson(
    "/api/enrich/azure",
    {
      app_id: els.azureAppId.value,
      lookback_minutes: Number(els.azureLookback.value || 30),
    },
    els.azureBtn,
    "Querying Application Insights..."
  );
});

els.copilotBtn.addEventListener("click", async () => {
  try {
    const payload = await postJson(
      "/api/copilot/run",
      { prompt: els.promptBox.textContent },
      els.copilotBtn,
      "Handing off investigation brief to Copilot..."
    );
    if (payload) {
      els.copilotOutput.textContent = payload.output || `Copilot exited with code ${payload.exit_code}`;
      setStatus(`Copilot finished with exit code ${payload.exit_code}.`);
    }
  } catch {
    els.copilotOutput.textContent = "Copilot execution failed. Check status above.";
  }
});

els.demoPlayBtn.addEventListener("click", startDemo);
els.demoReplayBtn.addEventListener("click", startDemo);

fetchState().catch((error) => setStatus(error.message, true));
