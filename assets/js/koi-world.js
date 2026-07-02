/* 锦鲤界 - 赛博修仙 JavaScript 框架 */
/* Cyber-Xianxia JS Framework for 锦鲤宗 IP World */

(function() {
  'use strict';

  /* ===== 粒子系统 ===== */
  class ParticleSystem {
    constructor(canvas) {
      this.canvas = canvas;
      this.ctx = canvas.getContext('2d');
      this.particles = [];
      this.resize();
      this.init();
      this.animate();
      window.addEventListener('resize', () => this.resize());
    }

    resize() {
      this.canvas.width = window.innerWidth;
      this.canvas.height = window.innerHeight;
    }

    init() {
      const count = Math.min(100, Math.floor(window.innerWidth / 20));
      for (let i = 0; i < count; i++) {
        this.particles.push({
          x: Math.random() * this.canvas.width,
          y: Math.random() * this.canvas.height,
          size: Math.random() * 2 + 0.5,
          speedX: (Math.random() - 0.5) * 0.5,
          speedY: (Math.random() - 0.5) * 0.5,
          opacity: Math.random() * 0.5 + 0.1,
          color: Math.random() > 0.5 ? '#00f0ff' : '#ffd700'
        });
      }
    }

    animate() {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      
      this.particles.forEach(p => {
        p.x += p.speedX;
        p.y += p.speedY;
        
        if (p.x < 0) p.x = this.canvas.width;
        if (p.x > this.canvas.width) p.x = 0;
        if (p.y < 0) p.y = this.canvas.height;
        if (p.y > this.canvas.height) p.y = 0;
        
        this.ctx.beginPath();
        this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        this.ctx.fillStyle = p.color;
        this.ctx.globalAlpha = p.opacity;
        this.ctx.fill();
      });
      
      this.ctx.globalAlpha = 1;
      requestAnimationFrame(() => this.animate());
    }
  }

  /* ===== 淡入动画观察器 ===== */
  class FadeInObserver {
    constructor() {
      this.observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
          }
        });
      }, { threshold: 0.1 });
      
      document.querySelectorAll('.fade-in').forEach(el => {
        this.observer.observe(el);
      });
    }
  }

  /* ===== 返回顶部 ===== */
  class BackToTop {
    constructor() {
      this.btn = document.createElement('div');
      this.btn.className = 'back-to-top';
      this.btn.innerHTML = '▲';
      document.body.appendChild(this.btn);
      
      window.addEventListener('scroll', () => this.toggle());
      this.btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }
    
    toggle() {
      if (window.scrollY > 500) {
        this.btn.classList.add('visible');
      } else {
        this.btn.classList.remove('visible');
      }
    }
  }

  /* ===== 标签页切换 ===== */
  class TabController {
    constructor() {
      document.querySelectorAll('.tab-nav').forEach(nav => {
        const buttons = nav.querySelectorAll('button');
        const tabGroup = nav.dataset.tabGroup || 'default';
        
        buttons.forEach(btn => {
          btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const target = btn.dataset.tab;
            document.querySelectorAll(`.tab-content[data-tab-group="${tabGroup}"]`).forEach(content => {
              content.classList.remove('active');
            });
            document.querySelector(`.tab-content[data-tab="${target}"][data-tab-group="${tabGroup}"]`)?.classList.add('active');
          });
        });
      });
    }
  }

  /* ===== 文字打字机效果 ===== */
  class TypeWriter {
    constructor(element, text, speed = 50) {
      this.element = element;
      this.text = text;
      this.speed = speed;
      this.index = 0;
      this.type();
    }
    
    type() {
      if (this.index < this.text.length) {
        this.element.textContent += this.text.charAt(this.index);
        this.index++;
        setTimeout(() => this.type(), this.speed);
      }
    }
  }

  /* ===== 鼠标轨迹光效 ===== */
  class MouseTrail {
    constructor() {
      this.trail = [];
      this.maxTrail = 20;
      document.addEventListener('mousemove', (e) => this.addPoint(e));
      this.animate();
    }
    
    addPoint(e) {
      this.trail.push({ x: e.clientX, y: e.clientY, age: 0 });
      if (this.trail.length > this.maxTrail) {
        this.trail.shift();
      }
    }
    
    animate() {
      this.trail.forEach(p => p.age++);
      this.trail = this.trail.filter(p => p.age < this.maxTrail);
      requestAnimationFrame(() => this.animate());
    }
  }

  /* ===== 导航高亮 ===== */
  function highlightNav() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-links a').forEach(link => {
      const href = link.getAttribute('href').split('/').pop();
      if (href === currentPage || (currentPage === '' && href === 'index.html')) {
        link.style.color = 'var(--cyan-primary)';
        link.style.background = 'rgba(0, 240, 255, 0.1)';
      }
    });
  }

  /* ===== 搜索功能 ===== */
  function initSearch() {
    const searchInput = document.querySelector('.search-input');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase();
      document.querySelectorAll('.searchable').forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(query) ? '' : 'none';
      });
    });
  }

  /* ===== 初始化 ===== */
  document.addEventListener('DOMContentLoaded', () => {
    // 粒子系统
    const canvas = document.getElementById('particles-canvas');
    if (canvas) {
      new ParticleSystem(canvas);
    }
    
    // 淡入动画
    new FadeInObserver();
    
    // 返回顶部
    new BackToTop();
    
    // 标签页
    new TabController();
    
    // 导航高亮
    highlightNav();
    
    // 搜索
    initSearch();
    
    // 锦鲤游动HTML注入
    if (!document.querySelector('.koi-swim')) {
      for (let i = 0; i < 3; i++) {
        const koi = document.createElement('div');
        koi.className = 'koi-swim';
        document.body.appendChild(koi);
      }
    }
  });

  /* ===== 全局工具函数 ===== */
  window.KoiWorld = {
    // 创建打字机效果
    typeWriter: (selector, text, speed) => {
      const el = document.querySelector(selector);
      if (el) new TypeWriter(el, text, speed);
    },
    
    // 平滑滚动到元素
    scrollTo: (selector) => {
      const el = document.querySelector(selector);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    },
    
    // 创建涟漪效果
    createRipple: (x, y) => {
      const ripple = document.createElement('div');
      ripple.style.cssText = `
        position: fixed;
        left: ${x}px;
        top: ${y}px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: rgba(0, 240, 255, 0.5);
        pointer-events: none;
        z-index: 9999;
        animation: rippleExpand 0.6s ease-out forwards;
      `;
      document.body.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    },
    
    // 闪烁文字效果
    glitchText: (element) => {
      const original = element.textContent;
      const chars = '0123456789ABCDEF';
      let iterations = 0;
      const interval = setInterval(() => {
        element.textContent = original
          .split('')
          .map((char, index) => {
            if (index < iterations) return original[index];
            return chars[Math.floor(Math.random() * chars.length)];
          })
          .join('');
        if (iterations >= original.length) clearInterval(interval);
        iterations += 1/3;
      }, 30);
    }
  };

  // 添加涟漪动画CSS
  const style = document.createElement('style');
  style.textContent = `
    @keyframes rippleExpand {
      to {
        width: 100px;
        height: 100px;
        margin-left: -50px;
        margin-top: -50px;
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(style);

})();
