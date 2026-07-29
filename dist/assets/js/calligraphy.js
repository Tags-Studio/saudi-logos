/**
 * Arabic Calligraphy AI Generator
 * Powered by Google Gemini Flash Image API (Nano Banana)
 * =====================================================
 */

// ──────────────────────────────────────────────────────
// 1. CALLIGRAPHY STYLE DEFINITIONS
//    Each style has: emoji, Arabic name, description,
//    and the English prompt suffix for Gemini
// ──────────────────────────────────────────────────────
const CALLIGRAPHY_STYLES = [
  {
    id: "naskh",
    emoji: "📜",
    nameAr: "خط النسخ",
    desc: "متوازن وواضح",
    prompt: "classical Arabic Naskh calligraphy script, clean balanced proportions, clear and highly legible letterforms, suitable for reading, traditional pen style",
    bgHint: "white background"
  },
  {
    id: "thuluth",
    emoji: "🕌",
    nameAr: "خط الثلث",
    desc: "أوتوماني كلاسيكي",
    prompt: "Ottoman Thuluth Arabic calligraphy, elongated majestic letterforms with traditional flourishes and diacritics, highly ornate and noble, mosque-inscription quality",
    bgHint: "white or cream background"
  },
  {
    id: "diwani",
    emoji: "🌿",
    nameAr: "خط الديواني",
    desc: "منحنيات بديعة",
    prompt: "Ottoman Diwani Arabic calligraphy script, flowing cursive style with ornate connecting strokes and elegant curves, decorative and artistic",
    bgHint: "white background"
  },
  {
    id: "ruqaa",
    emoji: "🖊️",
    nameAr: "خط الرقعة",
    desc: "يومي ومقروء",
    prompt: "Arabic Ruqa'a calligraphy script, compact practical everyday style, consistent letter sizes, clean and legible handwriting",
    bgHint: "white background"
  },
  {
    id: "kufic",
    emoji: "⬛",
    nameAr: "كوفي حديث",
    desc: "هندسي جريء",
    prompt: "modern geometric Kufic Arabic calligraphy, angular bold geometric letterforms, minimalist contemporary design, architectural quality",
    bgHint: "white or black background"
  },
  {
    id: "retro",
    emoji: "📺",
    nameAr: "ريترو عربي",
    desc: "عصر السبعينيات",
    prompt: "Arabic retro calligraphy style inspired by 1970s Arabic advertising and cinema posters, bold vintage typography with decorative elements",
    bgHint: "cream or aged paper background"
  },
  {
    id: "fluid",
    emoji: "💫",
    nameAr: "إنسيابي حديث",
    desc: "ناعم وعصري",
    prompt: "fluid modern Arabic lettering with smooth flowing organic curves, contemporary calligraphy fusion style, artistic and dynamic",
    bgHint: "white background"
  },
  {
    id: "khatam",
    emoji: "💎",
    nameAr: "خاتم ختم",
    desc: "مثالي للشعارات",
    prompt: "Arabic seal calligraphy (khatam style), circular or oval composition with intricate Arabic lettering suitable for a logo seal, ornamental borders",
    bgHint: "white background"
  }
];

// ──────────────────────────────────────────────────────
// 2. STATE
// ──────────────────────────────────────────────────────
let selectedStyle = CALLIGRAPHY_STYLES[0]; // Default to Naskh
let currentResultDataUrl = null;

// ──────────────────────────────────────────────────────
// 3. INIT — Render style cards and check saved API key
// ──────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  renderStyleCards();
  checkSavedApiKey();
});

function renderStyleCards() {
  const grid = document.getElementById("styles-grid");
  if (!grid) return;

  grid.innerHTML = CALLIGRAPHY_STYLES.map((style, i) => `
    <div class="style-card ${i === 0 ? "selected" : ""}"
         id="style-card-${style.id}"
         onclick="selectStyle('${style.id}')"
         role="radio"
         aria-checked="${i === 0}"
         tabindex="0"
         onkeydown="if(event.key==='Enter'||event.key===' ')selectStyle('${style.id}')">
      <div class="style-check">
        <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
      <span class="style-emoji">${style.emoji}</span>
      <span class="style-name">${style.nameAr}</span>
      <span class="style-desc">${style.desc}</span>
    </div>
  `).join("");
}

function selectStyle(id) {
  const style = CALLIGRAPHY_STYLES.find(s => s.id === id);
  if (!style) return;

  // Deselect all
  document.querySelectorAll(".style-card").forEach(card => {
    card.classList.remove("selected");
    card.setAttribute("aria-checked", "false");
  });

  // Select this one
  const card = document.getElementById(`style-card-${id}`);
  if (card) {
    card.classList.add("selected");
    card.setAttribute("aria-checked", "true");
  }

  selectedStyle = style;
}

// ──────────────────────────────────────────────────────
// 4. API KEY MANAGEMENT
// ──────────────────────────────────────────────────────
function checkSavedApiKey() {
  const saved = localStorage.getItem("gemini_api_key");
  const input = document.getElementById("api-key-input");
  const clearBtn = document.getElementById("clear-api-key");
  const statusEl = document.getElementById("api-key-status");

  if (saved && saved.length > 5) {
    input.value = saved;
    if (clearBtn) clearBtn.style.display = "inline-flex";
    if (statusEl) {
      statusEl.style.display = "block";
      statusEl.innerHTML = `<span style="color: var(--accent-green);">✓ مفتاح API محفوظ ومفعّل — ${saved.substring(0, 8)}...${saved.slice(-4)}</span>`;
    }
  }
}

function saveApiKey() {
  const input = document.getElementById("api-key-input");
  const clearBtn = document.getElementById("clear-api-key");
  const statusEl = document.getElementById("api-key-status");
  
  // Clean key from extra spaces, single/double quotes often pasted by mistake
  let key = input.value.trim().replace(/^["']|["']$/g, "").trim();

  if (!key || key.length < 10) {
    if (statusEl) {
      statusEl.style.display = "block";
      statusEl.innerHTML = `<span style="color: #ef4444;">⚠️ الرجاء إدخال مفتاح API صالح.</span>`;
    }
    return;
  }

  // Update input value with cleaned key
  input.value = key;

  localStorage.setItem("gemini_api_key", key);
  if (clearBtn) clearBtn.style.display = "inline-flex";
  
  if (statusEl) {
    statusEl.style.display = "block";
    if (!key.startsWith("AIza")) {
      statusEl.innerHTML = `<span style="color: #f59e0b;">⚠️ تم حفظ المفتاح بنجاح، لكنه لا يبدأ بـ "AIza". قد لا يعمل بشكل صحيح إذا لم يكن مفتاح Gemini API.</span>`;
    } else {
      statusEl.innerHTML = `<span style="color: var(--accent-green);">✓ تم حفظ المفتاح بنجاح على جهازك — ${key.substring(0, 8)}...${key.slice(-4)}</span>`;
    }
  }
}

function clearApiKey() {
  localStorage.removeItem("gemini_api_key");
  const input = document.getElementById("api-key-input");
  const clearBtn = document.getElementById("clear-api-key");
  const statusEl = document.getElementById("api-key-status");
  if (input) input.value = "";
  if (clearBtn) clearBtn.style.display = "none";
  if (statusEl) {
    statusEl.style.display = "block";
    statusEl.innerHTML = `<span style="color: var(--text-secondary);">تم حذف المفتاح من جهازك</span>`;
  }
}

// ──────────────────────────────────────────────────────
// 5. ADVANCED OPTIONS TOGGLE
// ──────────────────────────────────────────────────────
let advancedOpen = false;
function toggleAdvanced() {
  advancedOpen = !advancedOpen;
  const panel = document.getElementById("advanced-options");
  const chevron = document.getElementById("advanced-chevron");
  if (panel) panel.style.display = advancedOpen ? "block" : "none";
  if (chevron) chevron.style.transform = advancedOpen ? "rotate(180deg)" : "rotate(0deg)";
}

// ──────────────────────────────────────────────────────
// 6. MAIN GENERATION FUNCTION
// ──────────────────────────────────────────────────────
async function generateCalligraphy() {
  const apiKey = localStorage.getItem("gemini_api_key");
  const textInput = document.getElementById("arabic-text-input");
  const text = textInput ? textInput.value.trim() : "";
  const bgColor = document.getElementById("bg-color-select")?.value || "white";
  const orientation = document.getElementById("orientation-select")?.value || "square centered";
  const extraPrompt = document.getElementById("extra-prompt")?.value.trim() || "";

  // ── Validation ──────────────────────────────────────
  if (!apiKey || apiKey.length < 10) {
    showError("الرجاء إدخال مفتاح Google AI Studio API أولاً.\nيمكنك الحصول على مفتاح مجاني من: https://aistudio.google.com/apikey");
    document.getElementById("api-key-input")?.focus();
    return;
  }

  if (!text) {
    textInput?.focus();
    showError("الرجاء كتابة النص العربي أولاً");
    return;
  }

  if (text.length > 120) {
    showError("النص طويل جداً. الحد الأقصى 120 حرف");
    return;
  }

  // ── Build Prompt ────────────────────────────────────
  const orientationNote = orientation === "square centered"
    ? "square 1:1 aspect ratio, centered composition"
    : orientation === "wide horizontal"
    ? "wide horizontal banner composition, 16:9 or 3:1 ratio"
    : "vertical tall composition, portrait orientation";

  const bgNote = bgColor === "transparent checkered"
    ? "transparent background (render on checkerboard to show transparency)"
    : `${bgColor} background`;

  const prompt = [
    `Create a professional Arabic calligraphy artwork.`,
    `The Arabic text to render is: "${text}"`,
    `Calligraphy style: ${selectedStyle.prompt}`,
    `Background: ${bgNote}`,
    `Composition: ${orientationNote}`,
    `Requirements: The Arabic text MUST be written correctly and completely, all letters properly connected in Arabic script, high artistic quality, high resolution detail suitable for printing or professional use, no spelling errors, all characters of the given text must appear.`,
    extraPrompt ? `Additional notes: ${extraPrompt}` : "",
    `Do not add any English text or labels in the image.`
  ].filter(Boolean).join("\n");

  // ── UI: Show loading ────────────────────────────────
  setGeneratingState(true);
  showSection("loading");

  // Rotating loading tips
  const tips = [
    "يستغرق التوليد من 5 إلى 20 ثانية...",
    "الذكاء الاصطناعي يرسم الحروف الآن...",
    "جاري إتقان التفاصيل الخطية...",
    "تقريباً انتهى، صبر جميل...",
  ];
  let tipIdx = 0;
  const tipEl = document.getElementById("loading-tip");
  const tipInterval = setInterval(() => {
    tipIdx = (tipIdx + 1) % tips.length;
    if (tipEl) tipEl.textContent = tips[tipIdx];
  }, 4000);

  // ── Call Gemini API ─────────────────────────────────
  try {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-preview-image-generation:generateContent?key=${apiKey}`;

    const body = {
      contents: [
        {
          parts: [
            { text: prompt }
          ]
        }
      ],
      generationConfig: {
        responseModalities: ["TEXT", "IMAGE"]
      }
    };

    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    clearInterval(tipInterval);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const msg = errorData?.error?.message || `خطأ في الاتصال (${response.status})`;
      throw new Error(msg);
    }

    const data = await response.json();

    // ── Extract image from response ─────────────────
    let imageBase64 = null;
    let imageMimeType = "image/png";

    const candidates = data?.candidates;
    if (!candidates || candidates.length === 0) {
      throw new Error("لم يتم توليد أي نتيجة. حاول مرة أخرى.");
    }

    const parts = candidates[0]?.content?.parts || [];
    for (const part of parts) {
      if (part.inlineData) {
        imageBase64 = part.inlineData.data;
        imageMimeType = part.inlineData.mimeType || "image/png";
        break;
      }
    }

    if (!imageBase64) {
      // Maybe text-only response (safety block or no image generated)
      const textPart = parts.find(p => p.text);
      const textContent = textPart?.text || "";
      throw new Error(
        textContent
          ? `لم يتم توليد صورة. رسالة الذكاء الاصطناعي: "${textContent.substring(0, 200)}"`
          : "لم يتم توليد أي صورة. حاول بنص مختلف أو أسلوب آخر."
      );
    }

    // ── Show image ──────────────────────────────────
    const dataUrl = `data:${imageMimeType};base64,${imageBase64}`;
    currentResultDataUrl = dataUrl;

    const imgEl = document.getElementById("result-image");
    if (imgEl) {
      imgEl.src = dataUrl;
      imgEl.alt = `خط عربي ${selectedStyle.nameAr}: ${text}`;
    }

    const labelEl = document.getElementById("result-style-label");
    if (labelEl) labelEl.textContent = `${selectedStyle.emoji} ${selectedStyle.nameAr}`;

    showSection("success");

  } catch (err) {
    clearInterval(tipInterval);
    console.error("Calligraphy generation error:", err);
    showError(err.message || "حدث خطأ غير متوقع. الرجاء المحاولة مرة أخرى.");
  } finally {
    setGeneratingState(false);
  }
}

// ──────────────────────────────────────────────────────
// 7. DOWNLOAD
// ──────────────────────────────────────────────────────
function downloadImage() {
  if (!currentResultDataUrl) return;

  const text = document.getElementById("arabic-text-input")?.value.trim() || "calligraphy";
  const styleName = selectedStyle.id;
  const filename = `saudi-logos-calligraphy-${styleName}-${Date.now()}.png`;

  const a = document.createElement("a");
  a.href = currentResultDataUrl;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

// ──────────────────────────────────────────────────────
// 8. UI HELPERS
// ──────────────────────────────────────────────────────
function setGeneratingState(isGenerating) {
  const btn = document.getElementById("generate-btn");
  const icon = document.getElementById("generate-icon");
  const text = document.getElementById("generate-text");
  if (!btn) return;

  btn.disabled = isGenerating;

  if (isGenerating) {
    btn.style.opacity = "0.7";
    btn.style.cursor = "not-allowed";
    if (text) text.textContent = "⏳ جاري التوليد...";
    if (icon) icon.style.animation = "calligraphySpin 1s linear infinite";
  } else {
    btn.style.opacity = "1";
    btn.style.cursor = "pointer";
    if (text) text.textContent = "✨ توليد التصميم الآن";
    if (icon) icon.style.animation = "";
  }
}

function showSection(section) {
  const resultSection = document.getElementById("result-section");
  const loading = document.getElementById("loading-state");
  const error = document.getElementById("error-state");
  const success = document.getElementById("success-state");

  if (resultSection) resultSection.style.display = "block";

  // Hide all sub-states
  if (loading) loading.style.display = "none";
  if (error) error.style.display = "none";
  if (success) success.style.display = "none";

  // Show target
  if (section === "loading" && loading) {
    loading.style.display = "block";
  } else if (section === "error" && error) {
    error.style.display = "block";
  } else if (section === "success" && success) {
    success.style.display = "block";
    // Scroll into view smoothly
    resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

function showError(message) {
  const msgEl = document.getElementById("error-message");
  if (msgEl) msgEl.textContent = message;
  showSection("error");
}
