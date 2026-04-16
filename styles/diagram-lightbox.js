(function () {
  "use strict";

  var ENHANCED = "diagramLightboxEnhanced";
  var zoom = 1;
  var overlay = null;
  var diagramSlot = null;

  function candidateDiagrams() {
    return Array.prototype.slice
      .call(document.querySelectorAll(".mermaid"))
      .filter(function (node) {
        return !node.closest(".diagram-lightbox");
      });
  }

  function renderedSvg(diagram) {
    if (!diagram) {
      return null;
    }
    if (diagram.tagName && diagram.tagName.toLowerCase() === "svg") {
      return diagram;
    }
    return (
      diagram.querySelector("svg") ||
      (diagram.parentElement && diagram.parentElement.querySelector("svg"))
    );
  }

  function diagramSource(diagram) {
    var code = diagram.querySelector("code");
    if (code) {
      return code.textContent;
    }
    return diagram.textContent;
  }

  function ensureOverlay() {
    if (overlay) {
      return overlay;
    }

    overlay = document.createElement("div");
    overlay.className = "diagram-lightbox";
    overlay.hidden = true;
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", "Expanded diagram");

    var toolbar = document.createElement("div");
    toolbar.className = "diagram-lightbox__toolbar";
    toolbar.addEventListener("click", function (event) {
      event.stopPropagation();
    });

    var zoomOut = lightboxButton("Zoom out", "-");
    var zoomIn = lightboxButton("Zoom in", "+");
    var reset = lightboxButton("Reset zoom", "Reset");
    var close = lightboxButton("Close diagram", "Close");

    zoomOut.addEventListener("click", function () {
      setZoom(Math.max(0.6, zoom - 0.2));
    });
    zoomIn.addEventListener("click", function () {
      setZoom(Math.min(3, zoom + 0.2));
    });
    reset.addEventListener("click", function () {
      setZoom(1);
    });
    close.addEventListener("click", closeOverlay);

    toolbar.appendChild(zoomOut);
    toolbar.appendChild(zoomIn);
    toolbar.appendChild(reset);
    toolbar.appendChild(close);

    var viewport = document.createElement("div");
    viewport.className = "diagram-lightbox__viewport";
    viewport.addEventListener("click", function (event) {
      event.stopPropagation();
    });

    diagramSlot = document.createElement("div");
    diagramSlot.className = "diagram-lightbox__diagram";
    viewport.appendChild(diagramSlot);

    overlay.appendChild(toolbar);
    overlay.appendChild(viewport);
    overlay.addEventListener("click", closeOverlay);
    document.body.appendChild(overlay);

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && overlay && !overlay.hidden) {
        closeOverlay();
      }
    });

    return overlay;
  }

  function lightboxButton(label, text) {
    var button = document.createElement("button");
    button.type = "button";
    button.className = "diagram-lightbox__button";
    button.setAttribute("aria-label", label);
    button.textContent = text;
    return button;
  }

  function setZoom(nextZoom) {
    zoom = Math.round(nextZoom * 10) / 10;
    if (diagramSlot) {
      diagramSlot.style.setProperty("--diagram-lightbox-zoom", String(zoom));
      refreshScaledLayout();
    }
  }

  function refreshScaledLayout() {
    var rendered = diagramSlot && diagramSlot.querySelector(".diagram-lightbox__rendered");
    if (!rendered) {
      return;
    }

    var bounds = rendered.getBoundingClientRect();
    var unscaledWidth = bounds.width / zoom;
    var unscaledHeight = bounds.height / zoom;

    diagramSlot.style.setProperty(
      "--diagram-lightbox-layout-width",
      Math.ceil(unscaledWidth * zoom) + "px"
    );
    diagramSlot.style.setProperty(
      "--diagram-lightbox-layout-height",
      Math.ceil(unscaledHeight * zoom) + "px"
    );
  }

  function closeOverlay() {
    if (!overlay) {
      return;
    }
    overlay.hidden = true;
    document.body.classList.remove("diagram-lightbox-open");
    if (diagramSlot) {
      diagramSlot.replaceChildren();
    }
  }

  function openOverlay(container, source) {
    ensureOverlay();
    var svg = renderedSvg(container);
    if (svg) {
      var rendered = document.createElement("div");
      rendered.className = "diagram-lightbox__rendered";
      rendered.appendChild(svg.cloneNode(true));
      diagramSlot.replaceChildren(rendered);
      openReadyOverlay();
      return;
    }

    if (window.mermaid && typeof window.mermaid.render === "function") {
      renderMermaidSource(source);
      return;
    }

    var fallback = document.createElement("pre");
    fallback.className = "diagram-lightbox__source";
    fallback.textContent = source;
    diagramSlot.replaceChildren(fallback);
    openReadyOverlay();
  }

  function openReadyOverlay() {
    setZoom(1);
    overlay.hidden = false;
    document.body.classList.add("diagram-lightbox-open");
    window.requestAnimationFrame(refreshScaledLayout);
  }

  function renderMermaidSource(source) {
    var renderId = "diagram-lightbox-" + Date.now().toString(36);
    Promise.resolve(window.mermaid.render(renderId, source))
      .then(function (result) {
        var rendered = document.createElement("div");
        rendered.className = "diagram-lightbox__rendered";
        rendered.innerHTML = result.svg || result;
        diagramSlot.replaceChildren(rendered);
        openReadyOverlay();
      })
      .catch(function () {
        var fallback = document.createElement("pre");
        fallback.className = "diagram-lightbox__source";
        fallback.textContent = source;
        diagramSlot.replaceChildren(fallback);
        openReadyOverlay();
      });
  }

  function enhanceDiagram(diagram) {
    if (diagram.dataset[ENHANCED] === "true") {
      return;
    }

    var host = document.createElement("div");
    host.className = "diagram-zoom-host";
    var source = diagramSource(diagram);
    diagram.parentNode.insertBefore(host, diagram);
    host.appendChild(diagram);

    var button = document.createElement("button");
    button.type = "button";
    button.className = "diagram-zoom-button";
    button.textContent = "Open larger";
    button.setAttribute("aria-label", "Open diagram in a larger overlay");
    button.addEventListener("click", function () {
      openOverlay(host, source);
    });

    host.appendChild(button);
    diagram.dataset[ENHANCED] = "true";
  }

  function enhanceDiagrams() {
    candidateDiagrams().forEach(enhanceDiagram);
  }

  function scheduleEnhancement() {
    enhanceDiagrams();
    window.setTimeout(enhanceDiagrams, 250);
    window.setTimeout(enhanceDiagrams, 1000);
  }

  function observeMermaidRendering() {
    if (!window.MutationObserver) {
      return;
    }
    var observer = new MutationObserver(function () {
      enhanceDiagrams();
    });
    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      scheduleEnhancement();
      observeMermaidRendering();
    });
  } else {
    scheduleEnhancement();
    observeMermaidRendering();
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(scheduleEnhancement);
  }
})();
