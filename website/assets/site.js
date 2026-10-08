(() => {
  const root = document.documentElement;
  const base = root.dataset.base;
  const modes = new Set(["zh", "en", "both"]);
  const menu = document.querySelector(".menu-toggle");
  const navigation = document.querySelector("#library-nav");
  const setMenu = (open) => {
    navigation.classList.toggle("is-open", open);
    menu.setAttribute("aria-expanded", String(open));
    menu.textContent = open ? "关闭" : "目录";
  };
  menu.addEventListener("click", () =>
    setMenu(menu.getAttribute("aria-expanded") !== "true"),
  );
  document.addEventListener("keydown", (event) => {
    if (
      event.key === "Escape" &&
      menu.getAttribute("aria-expanded") === "true"
    ) {
      setMenu(false);
      menu.focus();
    }
    if (
      event.key === "/" &&
      !event.metaKey &&
      !event.ctrlKey &&
      !/INPUT|TEXTAREA|SELECT/.test(event.target.tagName) &&
      !event.target.isContentEditable
    ) {
      event.preventDefault();
      if (document.querySelector("#query"))
        document.querySelector("#query").focus();
      else location.href = base + "search/";
    }
  });
  const scrollToAnchor = () => {
    if (!location.hash) return;
    let anchor;
    try {
      anchor = decodeURIComponent(location.hash.slice(1));
    } catch {
      return;
    }
    const direct = document.getElementById(anchor);
    const canonical = direct?.dataset.anchor || anchor;
    const id = root.dataset.language === "en" ? "en-" + canonical : canonical;
    const target = document.getElementById(id) || direct;
    if (!target) return;
    for (
      let parent = target.parentElement;
      parent;
      parent = parent.parentElement
    ) {
      if (parent.tagName === "DETAILS") parent.open = true;
    }
    target.scrollIntoView();
  };
  const setLanguage = (language) => {
    root.dataset.language = modes.has(language) ? language : "zh";
    document.querySelectorAll("button[data-language]").forEach((button) => {
      button.setAttribute(
        "aria-pressed",
        String(button.dataset.language === root.dataset.language),
      );
    });
  };
  try {
    setLanguage(localStorage.getItem("pstack-language"));
  } catch {
    setLanguage("zh");
  }
  document.querySelectorAll("button[data-language]").forEach((button) => {
    button.addEventListener("click", () => {
      const visibleHeadings = [
        ...document.querySelectorAll(".prose [data-anchor]"),
      ].filter((node) => node.getClientRects().length);
      const current = visibleHeadings
        .filter((node) => node.getBoundingClientRect().top <= 160)
        .at(-1);
      setLanguage(button.dataset.language);
      try {
        localStorage.setItem("pstack-language", root.dataset.language);
      } catch {}
      if (current && window.scrollY > 300) {
        const id =
          (root.dataset.language === "en" ? "en-" : "") +
          current.dataset.anchor;
        document.getElementById(id)?.scrollIntoView();
      }
    });
  });
  window.addEventListener("hashchange", scrollToAnchor);
  document
    .querySelectorAll('a[href^="#"]')
    .forEach((link) =>
      link.addEventListener("click", () =>
        requestAnimationFrame(scrollToAnchor),
      ),
    );
  requestAnimationFrame(scrollToAnchor);

  const form = document.querySelector("#search-form");
  if (!form) return;
  const input = document.querySelector("#query");
  const status = document.querySelector(".search-status");
  const results = document.querySelector("#search-results");
  let indexPromise;
  let request = 0;
  const loadIndex = () => {
    if (!indexPromise)
      indexPromise = fetch(base + "search.json")
        .then((response) => {
          if (!response.ok) throw new Error("search index unavailable");
          return response.json();
        })
        .catch((error) => {
          indexPromise = null;
          throw error;
        });
    return indexPromise;
  };
  const search = async () => {
    const current = ++request;
    const query = input.value.trim();
    const url = new URL(location.href);
    query ? url.searchParams.set("q", query) : url.searchParams.delete("q");
    history.replaceState(null, "", url);
    results.replaceChildren();
    if (!query) {
      status.textContent = "输入关键词，搜索中文与英文全文。";
      return;
    }
    status.textContent = "正在搜索…";
    try {
      const index = await loadIndex();
      if (current !== request) return;
      const words = query.toLocaleLowerCase().split(/\s+/).filter(Boolean);
      const found = index
        .map((doc) => {
          const heading = (doc.title + " " + doc.english).toLocaleLowerCase();
          const text = doc.text.toLocaleLowerCase();
          return {
            doc,
            score: words.every(
              (word) => text.includes(word) || heading.includes(word),
            )
              ? words.reduce(
                  (score, word) => score + (heading.includes(word) ? 20 : 1),
                  0,
                )
              : 0,
          };
        })
        .filter((item) => item.score)
        .sort((a, b) => b.score - a.score);
      status.textContent = `找到 ${found.length} 篇文档${found.length > 40 ? "，显示前 40 篇" : ""}。`;
      if (!found.length)
        status.textContent += " 试试更短的关键词，或技能的英文名称。";
      found.slice(0, 40).forEach(({ doc }) => {
        const item = document.createElement("li");
        const link = document.createElement("a");
        link.href = doc.url;
        const section = document.createElement("small");
        section.textContent = doc.section;
        const title = document.createElement("h2");
        title.textContent = doc.title;
        const english = document.createElement("p");
        english.textContent = doc.english;
        const snippet = document.createElement("p");
        const match = doc.text.toLocaleLowerCase().indexOf(words[0]);
        const start = Math.max(0, match - 45);
        snippet.textContent =
          (start ? "…" : "") + doc.text.slice(start, start + 170) + "…";
        link.append(section, title, english, snippet);
        item.append(link);
        results.append(item);
      });
    } catch {
      if (current === request)
        status.textContent = "搜索索引未能加载。请重试，或通过目录浏览。";
    }
  };
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    search();
  });
  let timer;
  input.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(search, 180);
  });
  input.value = new URLSearchParams(location.search).get("q") || "";
  if (input.value) search();
})();
