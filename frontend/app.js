const API = {
  config: "/api/config",
  sentiment: "/api/sentiment",
  rag: "/api/rag",
};

const state = {
  config: null,
  lastData: null,
  lastRunQuery: "",
  currentQuery: "",
};

const els = {
  tabButtons: document.querySelectorAll("[data-tab]"),
  tabPanels: document.querySelectorAll(".tab-panel"),
  form: document.querySelector("#ragForm"),
  query: document.querySelector("#query"),
  queryHint: document.querySelector("#queryHint"),
  staleWarning: document.querySelector("#staleWarning"),
  topK: document.querySelector("#topK"),
  sentiment: document.querySelector("#sentiment"),
  category: document.querySelector("#category"),
  ratingFilter: document.querySelector("#ratingFilter"),
  autoFilter: document.querySelector("#autoFilter"),
  smartCategory: document.querySelector("#smartCategory"),
  excludeApp: document.querySelector("#excludeApp"),
  evidenceOnly: document.querySelector("#evidenceOnly"),
  submitBtn: document.querySelector("#submitBtn"),
  buttonText: document.querySelector("#buttonText"),
  buttonSpinner: document.querySelector("#buttonSpinner"),
  ragStatus: document.querySelector("#ragStatus"),
  understandingPanel: document.querySelector("#understandingPanel"),
  understandingGrid: document.querySelector("#understandingGrid"),
  emptyState: document.querySelector("#emptyState"),
  loadingState: document.querySelector("#loadingState"),
  errorState: document.querySelector("#errorState"),
  errorMessage: document.querySelector("#errorMessage"),
  answerContent: document.querySelector("#answerContent"),
  answeredQuery: document.querySelector("#answeredQuery"),
  summaryText: document.querySelector("#summaryText"),
  issueList: document.querySelector("#issueList"),
  compactEvidence: document.querySelector("#compactEvidence"),
  confidenceBox: document.querySelector("#confidenceBox"),
  confidenceLabel: document.querySelector("#confidenceLabel"),
  confidenceNote: document.querySelector("#confidenceNote"),
  topEvidenceList: document.querySelector("#topEvidenceList"),
  evidenceList: document.querySelector("#evidenceList"),
  extraEvidenceDetails: document.querySelector("#extraEvidenceDetails"),
  extraEvidenceList: document.querySelector("#extraEvidenceList"),
  resultCount: document.querySelector("#resultCount"),
  debugPanel: document.querySelector("#debugPanel"),
  sentimentReview: document.querySelector("#sentimentReview"),
  sentimentBtn: document.querySelector("#sentimentBtn"),
  sentimentResult: document.querySelector("#sentimentResult"),
  sentimentModelBadge: document.querySelector("#sentimentModelBadge"),
  docCount: document.querySelector("#docCount"),
  modelName: document.querySelector("#modelName"),
  modelCaption: document.querySelector("#modelCaption"),
  retrievalBadges: document.querySelector("#retrievalBadges"),
  precisionLabel: document.querySelector("#precisionLabel"),
  precisionAt5: document.querySelector("#precisionAt5"),
  precisionCaption: document.querySelector("#precisionCaption"),
  systemDetails: document.querySelector("#systemDetails"),
  downloadJson: document.querySelector("#downloadJson"),
  downloadMarkdown: document.querySelector("#downloadMarkdown"),
  downloadCsv: document.querySelector("#downloadCsv"),
};

function formatNumber(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "N/A";
  return new Intl.NumberFormat("vi-VN").format(Number(value));
}

function formatScore(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "N/A";
  return Number(value).toFixed(3);
}

function formatRating(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "N/A sao";
  return `${Number(value).toLocaleString("vi-VN", { maximumFractionDigits: 1 })} sao`;
}

function sentimentLabel(value) {
  const key = String(value || "").toLowerCase();
  if (key === "negative") return "Tiêu cực";
  if (key === "positive") return "Tích cực";
  if (key === "neutral") return "Trung lập";
  if (key === "all") return "Tất cả";
  if (key === "auto") return "Tự động";
  return value || "Không rõ";
}

function ratingFilterLabel(value) {
  if (value === "low") return "1-2 sao";
  if (value === "mid") return "3 sao";
  if (value === "high") return "4-5 sao";
  return "Tất cả";
}

function shortenModelName(value) {
  const text = String(value || "");
  return text.includes("/") ? text.split("/").pop() : text || "N/A";
}

function shortenPath(value) {
  const text = String(value ?? "");
  if (!text) return "N/A";
  const marker = text.includes("\\") ? "\\" : "/";
  const parts = text.split(/[\\/]+/).filter(Boolean);
  if (parts.length <= 3) return text;
  return `...${marker}${parts.slice(-3).join(marker)}`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function shortText(value, limit = 240) {
  const text = String(value ?? "").replace(/\s+/g, " ").trim();
  if (text.length <= limit) return text;
  return `${text.slice(0, limit - 3).trim()}...`;
}

function setRagStatus(label, type = "idle") {
  els.ragStatus.textContent = label;
  els.ragStatus.className = `status ${type}`;
}

function showAnswerState(name) {
  const states = ["emptyState", "loadingState", "errorState", "answerContent"];
  states.forEach((key) => els[key].classList.toggle("hidden", key !== name));
}

function setLoading(isLoading) {
  els.submitBtn.disabled = isLoading;
  els.buttonText.textContent = isLoading ? "Đang chạy..." : "Chạy RAG";
  els.buttonSpinner.classList.toggle("hidden", !isLoading);
}

function switchTab(tabId) {
  els.tabButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.tab === tabId);
  });
  els.tabPanels.forEach((panel) => {
    panel.classList.toggle("active", panel.id === tabId);
  });
}

function buildPayload() {
  return {
    query: els.query.value.trim(),
    top_k: Number(els.topK.value || 5),
    sentiment: els.sentiment.value,
    category: els.category.value || null,
    rating_filter: els.ratingFilter.value || "all",
    auto_filter: els.autoFilter.checked,
    smart_category: els.smartCategory.checked,
    exclude_app: els.excludeApp.checked ? true : null,
    evidence_only: els.evidenceOnly.checked,
    sentiment_source: els.sentiment.value === "auto" ? "auto_intent_filter" : "manual_filter",
  };
}

function inferQueryHint(query) {
  const q = query.toLowerCase();
  if (!q.trim()) return "Vui lòng nhập câu hỏi trước khi chạy RAG.";
  if (q.includes("giao") || q.includes("ship") || q.includes("vận chuyển")) {
    return "Gợi ý: hệ thống sẽ ưu tiên evidence liên quan đến giao hàng/vận chuyển.";
  }
  if (q.includes("lỗi") || q.includes("hỏng") || q.includes("chất lượng")) {
    return "Gợi ý: hệ thống sẽ ưu tiên evidence về chất lượng hoặc lỗi sản phẩm.";
  }
  if (q.includes("size") || q.includes("kích thước") || q.includes("không vừa")) {
    return "Gợi ý: lọc category thông minh có thể ưu tiên Fashion.";
  }
  if (q.includes("shop") || q.includes("hỗ trợ") || q.includes("phản hồi")) {
    return "Gợi ý: câu hỏi thuộc nhóm dịch vụ hoặc shop support.";
  }
  return "Câu hỏi ổn. Nếu kết quả yếu, hãy hỏi cụ thể hơn theo một aspect.";
}

function renderMetrics(config) {
  els.docCount.textContent = formatNumber(config.num_documents);
  els.modelName.textContent = shortenModelName(config.embedding_model);
  els.modelName.title = config.embedding_model || "";
  els.modelCaption.textContent = "Full name trong bảng kỹ thuật";
  els.precisionLabel.textContent = config.precision_source === "baseline" ? "Baseline P@5" : (config.precision_label || "Precision@5");
  els.precisionAt5.textContent =
    config.precision_at_5 === null || config.precision_at_5 === undefined
      ? "N/A"
      : Number(config.precision_at_5).toFixed(3);
  els.precisionCaption.textContent = config.precision_source === "baseline"
    ? "Manual evaluation"
    : (config.precision_file ? shortenPath(config.precision_file) : "Chưa có file metric");
  els.sentimentModelBadge.textContent = config.sentiment_model ? "Model sẵn sàng" : "Model N/A";
}

function renderSystemDetails(config) {
  const rows = {
    "Kho review": `${formatNumber(config.num_documents)} review/documents`,
    "Embedding model": shortenModelName(config.embedding_model),
    "Full model name": config.embedding_model || "N/A",
    "Retrieval method": config.retrieval_method || "Dense FAISS + query expansion + lightweight rerank",
    "Precision@5": config.precision_at_5 === null || config.precision_at_5 === undefined ? "N/A" : Number(config.precision_at_5).toFixed(3),
    "Nguồn Precision@5": config.precision_source === "baseline" ? "Baseline/manual evaluation" : (config.precision_source || "N/A"),
    "FAISS index": "models/module4/review_faiss.index",
    "Metadata": "models/module4/review_metadata.parquet",
    "Sentiment model": config.sentiment_model || "models/module2/best_model.joblib",
    "Ghi chú": "Sentiment trong RAG là metadata/filter; câu hỏi RAG không được phân tích như review.",
  };
  els.systemDetails.innerHTML = Object.entries(rows)
    .map(([label, value]) => `
      <div class="debug-item">
        <span>${escapeHtml(label)}</span>
        <code>${escapeHtml(value)}</code>
      </div>
    `)
    .join("");
}

function renderCategoryOptions(categories = {}) {
  const names = Object.keys(categories).filter((name) => name && name !== "unknown");
  const preferred = ["Fashion", "Electronic", "Mobile", "HealthBeauty", "Cosmetic", "HomeLifestyle", "BabiesToys", "App"];
  const sorted = [
    ...preferred.filter((name) => names.includes(name)),
    ...names.filter((name) => !preferred.includes(name)).sort(),
  ];
  els.category.innerHTML = `<option value="">Tất cả</option>` + sorted
    .map((name) => `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`)
    .join("");
}

async function loadConfig() {
  try {
    const response = await fetch(API.config);
    if (!response.ok) throw new Error(await response.text());
    const config = await response.json();
    state.config = config;
    renderMetrics(config);
    renderSystemDetails(config);
    renderCategoryOptions(config.categories || {});
  } catch (error) {
    setRagStatus("Backend chưa sẵn sàng", "error");
    renderError("Không load được backend. Kiểm tra terminal đang chạy webapp.");
    console.error(error);
  }
}

function renderUnderstanding(data) {
  const u = data.understanding || {};
  const diagnostics = data.diagnostics || {};
  const cards = [
    ["Câu hỏi đang trả lời", u.answered_query || data.query || state.lastRunQuery],
    ["Chủ đề", u.aspect || "Tổng quát"],
    ["Cảm xúc ưu tiên", u.sentiment_filter || "Tất cả"],
    ["Ngành hàng", u.category_filter || "Tất cả"],
    ["Top K", u.top_k || diagnostics.top_k || "N/A"],
    ["Query mở rộng", u.expanded_query || diagnostics.expanded_query || "N/A"],
    ["Lý do filter", u.filter_reason || "Không có"],
  ];
  els.understandingGrid.innerHTML = cards
    .map(([label, value]) => `
      <div class="understanding-card">
        <span>${escapeHtml(label)}</span>
        <strong>${escapeHtml(value)}</strong>
      </div>
    `)
    .join("");
  els.understandingPanel.classList.remove("hidden");
}

function renderAnswerPanel(data) {
  els.answeredQuery.textContent = `Kết quả cho câu hỏi: "${data.query || state.lastRunQuery}"`;
  els.summaryText.textContent = data.summary || "Chưa đủ bằng chứng rõ ràng từ các review được truy xuất.";

  const issues = data.main_issues || [];
  if (!issues.length) {
    els.issueList.innerHTML = `<li>Chưa đủ bằng chứng rõ ràng từ các review được truy xuất.</li>`;
  } else {
    els.issueList.innerHTML = issues
      .slice(0, 5)
      .map((issue) => {
        const citations = (issue.citations || [])
          .slice(0, 3)
          .map((c) => `<span class="citation-inline">${escapeHtml(c)}</span>`)
          .join("");
        return `<li>${escapeHtml(issue.issue)} ${citations}</li>`;
      })
      .join("");
  }

  const evidence = data.evidence || [];
  els.compactEvidence.innerHTML = evidence.slice(0, 3)
    .map((item) => `
      <blockquote class="compact-quote">
        <strong>${escapeHtml(item.citation)}</strong>
        ${escapeHtml(formatRating(item.rating))}, ${escapeHtml(sentimentLabel(item.sentiment))}, Ngành hàng: ${escapeHtml(item.category || "Không rõ")}<br />
        “${escapeHtml(shortText(item.excerpt || item.comment, 190))}”
      </blockquote>
    `)
    .join("") || `<p>Chưa đủ bằng chứng rõ ràng từ các review được truy xuất.</p>`;

  const confidence = data.confidence || {};
  els.confidenceLabel.textContent = confidence.label || "N/A";
  const note = confidence.warning
    || `Số review được dùng: ${confidence.evidence_count ?? evidence.length}. Lưu ý: Câu trả lời chỉ dựa trên review được truy xuất, không suy diễn ngoài dữ liệu.`;
  els.confidenceNote.textContent = note;
  els.confidenceBox.dataset.level = confidence.level || "unknown";
}

function keywordsFromQuery(query) {
  const groups = [
    ["giao", "ship", "vận chuyển", "chậm", "trễ", "lâu"],
    ["thiếu", "phụ kiện", "không đủ"],
    ["sai", "nhầm", "không đúng", "không giống"],
    ["lỗi", "hỏng", "hư", "không hoạt động"],
    ["đóng gói", "bao bì", "móp", "vỡ", "bể"],
    ["size", "kích thước", "chật", "rộng", "không vừa"],
    ["shop", "hỗ trợ", "phản hồi", "rep", "tư vấn"],
  ];
  const q = query.toLowerCase();
  return groups.flatMap((group) => group.filter((word) => q.includes(word))).slice(0, 8);
}

function highlightKeywords(text, query) {
  let escaped = escapeHtml(text);
  for (const keyword of keywordsFromQuery(query)) {
    const pattern = new RegExp(`(${keyword.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")})`, "gi");
    escaped = escaped.replace(pattern, "<mark>$1</mark>");
  }
  return escaped;
}

function evidenceCard(item, idx) {
  const sentimentClass = String(item.sentiment || "").toLowerCase();
  const text = item.comment || item.excerpt || "";
  const needsMore = text.length > 260;
  return `
    <article class="evidence-card" data-card="${idx}">
      <header>
        <span class="citation">${escapeHtml(item.citation)}</span>
        <span class="score-badge" title="Độ liên quan sau rerank">Điểm liên quan ${formatScore(item.score)}</span>
      </header>
      <h3>${escapeHtml(item.product_name || "Không rõ sản phẩm")}</h3>
      <div class="meta-row">
        <span class="meta-badge">Ngành hàng: ${escapeHtml(item.category || "Không rõ")}</span>
        <span class="meta-badge">Số sao: ${escapeHtml(formatRating(item.rating))}</span>
        <span class="meta-badge ${escapeHtml(sentimentClass)}">Cảm xúc: ${escapeHtml(sentimentLabel(item.sentiment))}</span>
      </div>
      <p class="review-text">${highlightKeywords(text, state.lastRunQuery)}</p>
      ${needsMore ? `<button class="show-more" type="button" data-toggle="${idx}">Xem thêm</button>` : ""}
    </article>
  `;
}

function bindShowMore() {
  document.querySelectorAll("[data-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const card = document.querySelector(`[data-card="${button.dataset.toggle}"]`);
      const expanded = card.classList.toggle("expanded");
      button.textContent = expanded ? "Thu gọn" : "Xem thêm";
    });
  });
}

function renderTopEvidence(items = []) {
  const top = items.slice(0, 3);
  els.topEvidenceList.innerHTML = top.length
    ? top.map((item) => `
      <div class="mini-evidence">
        <strong>${escapeHtml(item.citation)} ${escapeHtml(sentimentLabel(item.sentiment))}</strong>
        <span>${escapeHtml(formatRating(item.rating))} · ${escapeHtml(item.category || "Không rõ")}</span>
        <p>${escapeHtml(shortText(item.excerpt || item.comment, 150))}</p>
      </div>
    `).join("")
    : `<p class="muted-text">Chưa có review tiêu biểu.</p>`;
}

function renderEvidenceCards(items = []) {
  els.resultCount.textContent = `${items.length} kết quả`;
  if (!items.length) {
    els.evidenceList.innerHTML = `
      <div class="state-card">
        <strong>Không tìm thấy review phù hợp</strong>
        <p>Thử bỏ bớt filter, tăng Top K, hoặc hỏi cụ thể hơn.</p>
      </div>
    `;
    els.extraEvidenceDetails.classList.add("hidden");
    return;
  }

  const visible = items.slice(0, 6);
  const extra = items.slice(6);
  els.evidenceList.innerHTML = visible.map(evidenceCard).join("");
  if (extra.length) {
    els.extraEvidenceDetails.classList.remove("hidden");
    els.extraEvidenceDetails.querySelector("summary").textContent = `Xem thêm ${extra.length} review`;
    els.extraEvidenceList.innerHTML = extra.map((item, index) => evidenceCard(item, index + 6)).join("");
  } else {
    els.extraEvidenceDetails.classList.add("hidden");
    els.extraEvidenceList.innerHTML = "";
  }
  bindShowMore();
}

function renderDebugPanel(diagnostics = {}) {
  const explanations = {
    original_query: "Query gốc",
    expanded_query: "Query expanded",
    top_k: "Top K",
    filters_applied: "Filters",
    sentiment_source: "Nguồn sentiment filter",
    candidate_k: "Candidates",
    returned_rows: "Returned",
    embedding_model: "Embedding model",
    faiss_index_path: "FAISS index path",
    metadata_path: "Metadata path",
    retrieval_time_ms: "Thời gian truy xuất",
  };
  const entries = Object.entries(diagnostics);
  els.debugPanel.innerHTML = entries.length
    ? entries.map(([key, value]) => `
      <div class="debug-item">
        <span>${escapeHtml(explanations[key] || key)}</span>
        <code>${escapeHtml(typeof value === "object" ? JSON.stringify(value) : shortenPath(value))}${key === "retrieval_time_ms" ? " ms" : ""}</code>
      </div>
    `).join("")
    : "<p>Chưa có chi tiết kỹ thuật.</p>";
}

function renderError(message) {
  showAnswerState("errorState");
  els.errorMessage.textContent = shortText(message, 280);
}

function renderSuccess(data) {
  const confidence = data.confidence || {};
  const statusType = confidence.level === "low" ? "weak" : "success";
  setRagStatus(confidence.level === "low" ? "Bằng chứng yếu" : "Hoàn tất", statusType);
  showAnswerState("answerContent");
  renderUnderstanding(data);
  renderAnswerPanel(data);
  renderTopEvidence(data.evidence || []);
  renderEvidenceCards(data.evidence || []);
  renderDebugPanel(data.diagnostics || {});
}

async function runRag(event) {
  event.preventDefault();
  const payload = buildPayload();
  state.currentQuery = payload.query;
  els.queryHint.textContent = inferQueryHint(payload.query);

  if (!payload.query) {
    setRagStatus("Thiếu câu hỏi", "error");
    renderError("Vui lòng nhập câu hỏi trước khi chạy RAG.");
    return;
  }

  state.lastRunQuery = payload.query;
  els.staleWarning.classList.add("hidden");
  setLoading(true);
  setRagStatus("Đang truy xuất...", "loading");
  showAnswerState("loadingState");
  els.understandingPanel.classList.add("hidden");
  els.evidenceList.innerHTML = "";
  els.extraEvidenceList.innerHTML = "";
  els.extraEvidenceDetails.classList.add("hidden");
  els.topEvidenceList.innerHTML = `<p class="muted-text">Đang tìm review tiêu biểu...</p>`;
  els.resultCount.textContent = "Đang chạy";
  renderDebugPanel({});

  try {
    const response = await fetch(API.rag, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || "Backend trả về lỗi.");
    }
    const data = await response.json();
    state.lastData = data;
    renderSuccess(data);
  } catch (error) {
    setRagStatus("Có lỗi", "error");
    renderError(error.message || "Không chạy được RAG.");
    console.error(error);
  } finally {
    setLoading(false);
  }
}

function renderSentimentPrediction(data) {
  const labelClass = String(data.label || "").toLowerCase();
  const margin = data.margin === null || data.margin === undefined ? "N/A" : Number(data.margin).toFixed(3);
  const confidence = data.confidence === null || data.confidence === undefined ? "N/A" : Number(data.confidence).toFixed(3);
  els.sentimentResult.className = `sentiment-result ${labelClass}`;
  els.sentimentResult.innerHTML = `
    <div>
      <span>Sentiment dự đoán</span>
      <strong>${escapeHtml(data.label_vi || sentimentLabel(data.label))}</strong>
    </div>
    <div>
      <span>Model đang dùng</span>
      <code>${escapeHtml(data.model_path || "models/module2/best_model.joblib")}</code>
    </div>
    <div>
      <span>Confidence/margin</span>
      <code>${escapeHtml(confidence)} / ${escapeHtml(margin)}</code>
    </div>
    <p>Gợi ý: đây là kết quả phân loại cảm xúc của một review, không phải phân tích câu hỏi RAG.</p>
  `;
}

async function runSentimentModel() {
  const text = els.sentimentReview.value.trim();
  if (!text) {
    els.sentimentResult.className = "sentiment-result error";
    els.sentimentResult.textContent = "Vui lòng nhập một review thật để phân tích sentiment.";
    return;
  }

  els.sentimentBtn.disabled = true;
  els.sentimentBtn.textContent = "Đang phân tích...";
  els.sentimentResult.className = "sentiment-result";
  els.sentimentResult.textContent = "Đang chạy Module 2 sentiment model...";

  try {
    const response = await fetch(API.sentiment, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || "Không chạy được sentiment model.");
    }
    const data = await response.json();
    renderSentimentPrediction(data);
  } catch (error) {
    els.sentimentResult.className = "sentiment-result error";
    els.sentimentResult.textContent = error.message || "Không chạy được sentiment model.";
    console.error(error);
  } finally {
    els.sentimentBtn.disabled = false;
    els.sentimentBtn.textContent = "Phân tích sentiment";
  }
}

function downloadText(filename, mimeType, text) {
  const blob = new Blob([text], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

function exportJson() {
  if (!state.lastData) return alert("Chưa có kết quả để export.");
  downloadText("rag_result.json", "application/json", JSON.stringify(state.lastData, null, 2));
}

function exportMarkdown() {
  if (!state.lastData) return alert("Chưa có kết quả để export.");
  downloadText("rag_answer.md", "text/markdown", state.lastData.answer || state.lastData.summary || "");
}

function exportCsv() {
  if (!state.lastData?.evidence?.length) return alert("Chưa có evidence để export.");
  const rows = state.lastData.evidence;
  const cols = ["citation", "score", "category", "product_name", "rating", "sentiment", "comment"];
  const csv = [
    cols.join(","),
    ...rows.map((row) => cols.map((col) => `"${String(row[col] ?? "").replaceAll('"', '""')}"`).join(",")),
  ].join("\n");
  downloadText("rag_evidence.csv", "text/csv", csv);
}

document.querySelectorAll("[data-query]").forEach((button) => {
  button.addEventListener("click", () => {
    els.query.value = button.dataset.query;
    els.queryHint.textContent = inferQueryHint(els.query.value);
    if (state.lastRunQuery && els.query.value.trim() !== state.lastRunQuery) {
      els.staleWarning.classList.remove("hidden");
    }
  });
});

els.query.addEventListener("input", () => {
  const query = els.query.value.trim();
  els.queryHint.textContent = inferQueryHint(query);
  els.staleWarning.classList.toggle("hidden", !state.lastRunQuery || query === state.lastRunQuery);
});

els.tabButtons.forEach((button) => {
  button.addEventListener("click", () => switchTab(button.dataset.tab));
});

els.form.addEventListener("submit", runRag);
els.sentimentBtn.addEventListener("click", runSentimentModel);
els.downloadJson.addEventListener("click", exportJson);
els.downloadMarkdown.addEventListener("click", exportMarkdown);
els.downloadCsv.addEventListener("click", exportCsv);
els.queryHint.textContent = inferQueryHint(els.query.value);
loadConfig();
