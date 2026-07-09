// theme-toggle, faq accordion, and search functionality

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initFAQ();
  initBackgroundToggle();
  initSearch();
  initToast();
  initHomeAutocomplete();
});

// --- Theme Management ---
function initTheme() {
  const themeToggle = document.getElementById('theme-toggle');
  if (!themeToggle) return;

  // Check saved theme or system preference
  const savedTheme = localStorage.getItem('theme');
  const systemPrefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;

  if (savedTheme === 'light' || (!savedTheme && systemPrefersLight)) {
    document.body.classList.add('light-theme');
    updateThemeIcon('light');
  } else {
    document.body.classList.remove('light-theme');
    updateThemeIcon('dark');
  }

  themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('light-theme');
    const isLight = document.body.classList.contains('light-theme');
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
    updateThemeIcon(isLight ? 'light' : 'dark');
  });
}

function updateThemeIcon(theme) {
  const themeToggle = document.getElementById('theme-toggle');
  if (!themeToggle) return;
  if (theme === 'light') {
    themeToggle.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
      </svg>
    `; // Moon icon for switching to dark
    themeToggle.setAttribute('title', 'تفعيل المظهر الداكن');
  } else {
    themeToggle.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>
      </svg>
    `; // Sun icon for switching to light
    themeToggle.setAttribute('title', 'تفعيل المظهر الفاتح');
  }
}

// --- FAQ Accordion ---
function initFAQ() {
  const faqQuestions = document.querySelectorAll('.faq-question');
  faqQuestions.forEach(question => {
    question.addEventListener('click', () => {
      const item = question.parentElement;
      const isActive = item.classList.contains('active');
      
      // Close all items
      document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('active'));
      
      // Toggle current item
      if (!isActive) {
        item.classList.add('active');
      }
    });
  });
}

// --- Logo Detail Background Toggle ---
function initBackgroundToggle() {
  const toggles = document.querySelectorAll('.toggle-bg-btn');
  const previewDisplay = document.querySelector('.preview-display');
  
  if (!previewDisplay || toggles.length === 0) return;

  toggles.forEach(toggle => {
    toggle.addEventListener('click', () => {
      // Remove active from all
      toggles.forEach(btn => btn.classList.remove('active'));
      // Add active to current
      toggle.classList.add('active');
      
      // Apply background style
      if (toggle.classList.contains('toggle-white')) {
        previewDisplay.style.backgroundColor = '#ffffff';
        previewDisplay.style.backgroundImage = 'none';
      } else if (toggle.classList.contains('toggle-dark')) {
        previewDisplay.style.backgroundColor = '#0f172a';
        previewDisplay.style.backgroundImage = 'none';
      } else if (toggle.classList.contains('toggle-transparent')) {
        previewDisplay.style.backgroundColor = '#ffffff';
        previewDisplay.style.backgroundImage = 'linear-gradient(45deg, #e2e8f0 25%, transparent 25%), linear-gradient(-45deg, #e2e8f0 25%, transparent 25%), linear-gradient(45deg, transparent 75%, #e2e8f0 75%), linear-gradient(-45deg, transparent 75%, #e2e8f0 75%)';
        previewDisplay.style.backgroundSize = '14px 14px';
        previewDisplay.style.backgroundPosition = '0 0, 0 7px, 7px -7px, -7px 0px';
      }
    });
  });
}

// --- Search & Filter System (for browse.html and search bar redirect) ---
let logosDatabase = [];

async function initSearch() {
  const searchInput = document.getElementById('search-input');
  const browseGrid = document.getElementById('browse-logo-grid');
  
  // If not on browse page or home search, look for home redirection search
  if (!searchInput) return;

  // Read query parameter if any
  const urlParams = new URLSearchParams(window.location.search);
  const initialQuery = urlParams.get('q') || '';
  const initialCategory = urlParams.get('c') || 'all';

  // Set input value
  if (initialQuery) {
    searchInput.value = initialQuery;
  }

  // Fetch all logos database
  try {
    const response = await fetch('/logos.json');
    logosDatabase = await response.json();
    
    // Setup event listeners for filtering
    setupFilters(initialCategory);
    
    // Initial run
    filterAndRenderLogos();
    
    searchInput.addEventListener('input', () => {
      filterAndRenderLogos();
    });
  } catch (error) {
    console.error('Failed to load logos database:', error);
  }
}

function setupFilters(selectedCategory) {
  const filterButtons = document.querySelectorAll('.filter-btn');
  if (filterButtons.length === 0) return;

  // Set active category from URL
  filterButtons.forEach(btn => {
    const cat = btn.getAttribute('data-category');
    if (cat === selectedCategory) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }

    // Click event
    btn.addEventListener('click', () => {
      filterButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filterAndRenderLogos();
    });
  });

  // Calculate counts for categories in sidebar
  updateCategoryCounts();
}

function updateCategoryCounts() {
  const filterButtons = document.querySelectorAll('.filter-btn');
  filterButtons.forEach(btn => {
    const cat = btn.getAttribute('data-category');
    const countSpan = btn.querySelector('.filter-count');
    if (!countSpan) return;

    if (cat === 'all') {
      countSpan.textContent = logosDatabase.length;
    } else {
      const count = logosDatabase.filter(logo => logo.category === cat).length;
      countSpan.textContent = count;
    }
  });
}

function filterAndRenderLogos() {
  const searchInput = document.getElementById('search-input');
  const activeFilterBtn = document.querySelector('.filter-btn.active');
  const browseGrid = document.getElementById('browse-logo-grid');
  const resultCountSpan = document.getElementById('result-count');
  
  if (!browseGrid) return;

  const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
  const category = activeFilterBtn ? activeFilterBtn.getAttribute('data-category') : 'all';

  // Filter logic
  const filtered = logosDatabase.filter(logo => {
    const matchesSearch = 
      logo.name_ar.toLowerCase().includes(query) || 
      logo.name_en.toLowerCase().includes(query) || 
      logo.tags.some(tag => tag.toLowerCase().includes(query)) ||
      logo.description.toLowerCase().includes(query);
      
    const matchesCategory = category === 'all' || logo.category === category;

    return matchesSearch && matchesCategory;
  });

  // Update count text
  if (resultCountSpan) {
    resultCountSpan.textContent = `تم العثور على ${filtered.length} شعار`;
  }

  // Render cards
  if (filtered.length === 0) {
    browseGrid.innerHTML = `
      <div class="no-results" style="grid-column: 1 / -1;">
        <div class="no-results-icon">🔍</div>
        <div class="no-results-text">لم يتم العثور على نتائج</div>
        <div class="no-results-subtext">جرب البحث بكلمات أخرى أو تصفح الأقسام الجانبية للوصول للشعار المطلوب.</div>
      </div>
    `;
    return;
  }

  // Categories translation map for badges
  const catNames = {
    'government': 'جهات حكومية',
    'private': 'شركات وخاص',
    'education': 'تعليم وجامعات',
    'sports': 'رياضة وأندية',
    'vision': 'مشاريع ورؤية'
  };

  browseGrid.innerHTML = filtered.map(logo => {
    const escapedName = logo.name_ar.replace(/'/g, "\\'");
    return `
    <div class="logo-card">
      <button class="fav-btn" data-slug="${logo.slug}" onclick="event.preventDefault(); event.stopPropagation(); toggleFavorite('${logo.slug}', '${escapedName}', '${logo.svg_path}')" title="إضافة للحقيبة">
        <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
        </svg>
      </button>
      <a href="/logos/${logo.slug}">
        <div class="logo-preview-box">
          <img src="${logo.svg_path}" alt="${logo.name_ar}" class="logo-preview-img" loading="lazy">
        </div>
      </a>
      <div class="logo-card-info">
        <span class="logo-card-cat">${catNames[logo.category] || logo.category}</span>
        <a href="/logos/${logo.slug}">
          <h3 class="logo-card-title">${logo.name_ar}</h3>
        </a>
        <div class="logo-card-meta">
          <span class="logo-card-downloads">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-left: 2px; vertical-align: middle;">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            ${logo.downloads.toLocaleString('ar-SA')} تحميل
          </span>
          <div class="logo-card-formats">
            <span class="format-badge">SVG</span>
            <span class="format-badge">PNG</span>
            <span class="format-badge">PDF</span>
          </div>
        </div>
      </div>
    </div>
    `;
  }).join('');
}

// --- Toast Notifications for download simulation ---
function initToast() {
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.id = 'download-toast';
  toast.innerHTML = `
    <span class="toast-icon">✓</span>
    <span class="toast-text">جاري بدء تحميل الملف...</span>
  `;
  document.body.appendChild(toast);

  // Expose download trigger globally so HTML onClick can use it
  window.triggerDownload = function(format, logoName) {
    window.showToast(`جاري تحميل شعار "${logoName}" بصيغة ${format.toUpperCase()}...`);
  };
  
  window.showToast = function(message, isSuccess = true) {
    const icon = toast.querySelector('.toast-icon');
    const text = toast.querySelector('.toast-text');
    icon.textContent = isSuccess ? '✓' : '✗';
    icon.style.color = isSuccess ? '#10b981' : '#ef4444';
    text.textContent = message;
    toast.classList.add('show');
    
    // Clear previous timeout if any
    if (window.toastTimeout) {
      clearTimeout(window.toastTimeout);
    }
    
    window.toastTimeout = setTimeout(() => {
      toast.classList.remove('show');
    }, 3000);
  };
}

// --- SVG Code Copying ---
window.copySvgCode = async function(svgPath, nameAr) {
  window.showToast("جاري جلب كود الشعار...");
  try {
    const response = await fetch(svgPath);
    if (!response.ok) throw new Error("Network response was not ok");
    const svgText = await response.text();
    
    // Copy to clipboard
    await navigator.clipboard.writeText(svgText);
    window.showToast(`تم نسخ كود شعار "${nameAr}" بنجاح! يمكنك لصقه الآن في Figma.`);
  } catch (error) {
    console.error("Failed to copy SVG:", error);
    window.showToast("عذراً، فشل نسخ كود الشعار.", false);
  }
};

// --- Share Card Generator ---
window.selectedGenBgColor = "#044e34";

window.selectGenBg = function(color, btnElement) {
  // Remove active from sibling color buttons
  const container = btnElement.parentElement;
  container.querySelectorAll('.gen-bg-btn').forEach(btn => btn.classList.remove('active'));
  btnElement.classList.add('active');
  window.selectedGenBgColor = color;
};

window.generateShareCard = async function(svgPath, nameAr) {
  window.showToast("جاري توليد بطاقة المشاركة...");
  
  try {
    const format = document.getElementById('gen-format').value;
    const bgColor = window.selectedGenBgColor || "#044e34";
    
    // Set dimensions
    const width = format === 'square' ? 800 : 1080;
    const height = format === 'square' ? 800 : 1920;
    
    // Create canvas
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');
    
    // 1. Draw Background
    ctx.fillStyle = bgColor;
    ctx.fillRect(0, 0, width, height);
    
    // 2. Fetch SVG content and load as blob to avoid CORS issues on Canvas
    const response = await fetch(svgPath);
    if (!response.ok) throw new Error("Failed to fetch SVG");
    const svgText = await response.text();
    
    const blob = new Blob([svgText], {type: 'image/svg+xml;charset=utf-8'});
    const url = URL.createObjectURL(blob);
    
    const img = new Image();
    img.onload = () => {
      // 3. Draw SVG Image in center
      // Calculate drawing size (e.g. 55% of canvas width)
      const logoSize = width * 0.55;
      
      // Keep aspect ratio of loaded image if possible, otherwise square size
      let drawW = logoSize;
      let drawH = logoSize;
      const aspect = img.width / img.height;
      if (aspect > 1) {
        drawH = logoSize / aspect;
      } else {
        drawW = logoSize * aspect;
      }
      
      const x = (width - drawW) / 2;
      const y = (height - drawH) / 2 - (format === 'story' ? 100 : 0); // shift up slightly for story format to leave room for label
      
      ctx.drawImage(img, x, y, drawW, drawH);
      
      // 4. Draw Label (Optional decorative text for the brand at the bottom)
      ctx.font = "bold 28px 'Tajawal', sans-serif";
      ctx.fillStyle = bgColor === '#ffffff' ? '#0f172a' : '#ffffff';
      ctx.textAlign = "center";
      
      if (format === 'story') {
        ctx.fillText(nameAr, width / 2, y + drawH + 80);
        ctx.font = "normal 18px 'Tajawal', sans-serif";
        ctx.fillStyle = bgColor === '#ffffff' ? '#64748b' : 'rgba(255,255,255,0.6)';
        ctx.fillText("مكتبة شعارات السعودية", width / 2, height - 100);
      } else {
        // Draw small branding logo or text at bottom
        ctx.font = "normal 16px 'Tajawal', sans-serif";
        ctx.fillStyle = bgColor === '#ffffff' ? '#94a3b8' : 'rgba(255,255,255,0.4)';
        ctx.fillText("شعارات السعودية", width / 2, height - 40);
      }
      
      // 5. Trigger download
      const dataUrl = canvas.toDataURL("image/png");
      const a = document.createElement('a');
      a.href = dataUrl;
      a.download = `Saudi-Logos-${nameAr}-${format}.png`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      
      URL.revokeObjectURL(url);
      window.showToast("تم توليد وتحميل الصورة بنجاح!");
    };
    
    img.onerror = () => {
      window.showToast("عذراً، فشل تحميل ملف الـ SVG.", false);
    };
    
    img.src = url;
    
  } catch (error) {
    console.error("Card generation failed:", error);
    window.showToast("عذراً، فشل توليد بطاقة المشاركة.", false);
  }
};

// --- WhatsApp Verification Form Submission ---
window.submitUpdateViaWhatsapp = function(nameAr) {
  const verifyLink = document.getElementById('verify-link').value.trim();
  const updateNotes = document.getElementById('update-notes').value.trim();
  
  let message = `مرحباً، أود تقديم طلب توثيق أو تحديث لشعار "${nameAr}" في مكتبة شعارات السعودية.\n\n`;
  if (verifyLink) {
    message += `رابط المصدر للتحقق: ${verifyLink}\n\n`;
  }
  message += `ملاحظات وطلب التحديث:\n${updateNotes}`;
  
  const encodedMessage = encodeURIComponent(message);
  const whatsappUrl = `https://wa.me/966500000000?text=${encodedMessage}`;
  
  // Open in new window
  window.open(whatsappUrl, '_blank');
};

// --- Home Page Autocomplete suggestions dropdown ---
function initHomeAutocomplete() {
  const input = document.getElementById('home-search-input');
  const dropdown = document.getElementById('search-suggestions');
  if (!input || !dropdown) return;

  let allLogos = [];
  fetch('/logos.json')
    .then(r => r.json())
    .then(data => {
      allLogos = data;
    })
    .catch(err => console.error('Failed to load autocomplete DB:', err));

  input.addEventListener('input', () => {
    const query = input.value.trim().toLowerCase();
    if (!query) {
      dropdown.style.display = 'none';
      return;
    }

    // Filter matching logos by Arabic name, English name, or tags
    const matches = allLogos.filter(logo => {
      return (
        logo.name_ar.toLowerCase().includes(query) ||
        (logo.name_en && logo.name_en.toLowerCase().includes(query)) ||
        (logo.tags && logo.tags.some(t => t.toLowerCase().includes(query)))
      );
    }).slice(0, 6);

    if (matches.length === 0) {
      dropdown.innerHTML = `
        <div style="padding: 1rem; text-align: center; color: var(--text-secondary); font-size: 0.9rem;">
          لا توجد شعارات مطابقة للبحث
        </div>
      `;
    } else {
      dropdown.innerHTML = matches.map(logo => {
        let catText = 'شعار';
        if (logo.category === 'government') catText = 'جهة حكومية';
        else if (logo.category === 'private') catText = 'شركة / قطاع خاص';
        else if (logo.category === 'education') catText = 'تعليم وجامعات';
        else if (logo.category === 'sports') catText = 'نادي / رياضة';
        else if (logo.category === 'vision') catText = 'مشاريع ورؤية 2030';
        
        return `
          <a href="/logos/${logo.slug}" class="suggestion-item">
            <div style="width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; background: white; border-radius: 6px; padding: 0.25rem; margin-left: 1rem; flex-shrink: 0; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
              <img src="${logo.svg_path}" alt="${logo.name_ar}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
            </div>
            <div style="flex-grow: 1; text-align: right;">
              <div style="font-weight: 500; color: var(--text-primary); font-size: 0.95rem;">${logo.name_ar}</div>
              <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.15rem;">${catText}</div>
            </div>
          </a>
        `;
      }).join('');
    }

    dropdown.style.display = 'block';
  });

  // Close dropdown on click outside
  document.addEventListener('click', (e) => {
    if (!input.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.style.display = 'none';
    }
  });

  // Show dropdown on focus if input has text
  input.addEventListener('focus', () => {
    if (input.value.trim()) {
      dropdown.style.display = 'block';
    }
  });
}
