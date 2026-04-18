"""Micro-interactions and polish components for Opportunity Inbox Copilot.

This module provides reusable UI components and CSS animations for premium
micro-interactions that make the UI feel polished and responsive.

Includes:
- CSS animation snippets
- Loading state components
- Toast notification component
- Progress indicator component
- Card hover effect CSS
- Transition utilities
"""

# =============================================================================
# CSS ANIMATION SNIPPETS
# =============================================================================

CSS_ANIMATIONS = """
/* Smooth easing curves for natural motion */
:root {
    --ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
    --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
    --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
    --ease-out-expo: cubic-bezier(0.19, 1, 0.22, 1);
}

/* Fade In Animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-in {
    animation: fadeIn 0.5s var(--ease-smooth) forwards;
}

/* Staggered fade in for lists */
.fade-in-delay-1 { animation-delay: 0.1s; opacity: 0; animation-fill-mode: forwards; }
.fade-in-delay-2 { animation-delay: 0.2s; opacity: 0; animation-fill-mode: forwards; }
.fade-in-delay-3 { animation-delay: 0.3s; opacity: 0; animation-fill-mode: forwards; }
.fade-in-delay-4 { animation-delay: 0.4s; opacity: 0; animation-fill-mode: forwards; }
.fade-in-delay-5 { animation-delay: 0.5s; opacity: 0; animation-fill-mode: forwards; }
.fade-in-delay-6 { animation-delay: 0.6s; opacity: 0; animation-fill-mode: forwards; }

/* Slide In from Left */
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
}
.slide-in-left {
    animation: slideInLeft 0.4s var(--ease-out-expo) forwards;
}

/* Slide In from Right */
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(30px); }
    to { opacity: 1; transform: translateX(0); }
}
.slide-in-right {
    animation: slideInRight 0.4s var(--ease-out-expo) forwards;
}

/* Slide Up */
@keyframes slideUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.slide-up {
    animation: slideUp 0.3s var(--ease-smooth) forwards;
}

/* Pulse Animation for Loading States */
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(0.98); }
}
.pulse {
    animation: pulse 1.5s var(--ease-smooth) infinite;
}

/* Pulse with Shadow for Urgent Items */
@keyframes pulse-shadow {
    0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
    50% { box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
}
.pulse-shadow-critical {
    animation: pulse-shadow 2s var(--ease-smooth) infinite;
}

@keyframes pulse-shadow-urgent {
    0%, 100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.4); }
    50% { box-shadow: 0 0 0 6px rgba(245, 158, 11, 0); }
}
.pulse-shadow-urgent {
    animation: pulse-shadow-urgent 2s var(--ease-smooth) infinite;
}

/* Spinner Animation */
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
.spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(79, 70, 229, 0.1);
    border-top: 3px solid #4F46E5;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

.spinner-small {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(79, 70, 229, 0.1);
    border-top: 2px solid #4F46E5;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
}

/* Shimmer/Skeleton Loading */
@keyframes shimmer-skeleton {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
.skeleton {
    background: linear-gradient(90deg, #E5E7EB 0%, #F3F4F6 50%, #E5E7EB 100%);
    background-size: 200% 100%;
    animation: shimmer-skeleton 1.5s infinite;
    border-radius: 8px;
}

/* Animated Dots for Loading Text */
@keyframes dots {
    0%, 20% { content: '.'; }
    40% { content: '..'; }
    60%, 100% { content: '...'; }
}
.loading-dots::after {
    content: '.';
    animation: dots 1.5s infinite;
}

/* Checkmark Animation */
@keyframes checkmark {
    0% { transform: scale(0); opacity: 0; }
    50% { transform: scale(1.2); }
    100% { transform: scale(1); opacity: 1; }
}
.checkmark-animate {
    animation: checkmark 0.4s var(--ease-bounce) forwards;
}

/* Success Checkmark Draw Animation */
@keyframes checkmark-draw {
    0% { stroke-dashoffset: 100; }
    100% { stroke-dashoffset: 0; }
}
.checkmark-draw {
    stroke-dasharray: 100;
    stroke-dashoffset: 100;
    animation: checkmark-draw 0.5s var(--ease-smooth) 0.2s forwards;
}

/* Scale Pop Animation for Emphasis */
@keyframes pop {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}
.pop {
    animation: pop 0.3s var(--ease-spring) forwards;
}

/* Bounce Animation */
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}
.bounce {
    animation: bounce 0.6s var(--ease-spring) forwards;
}

/* Shake Animation for Errors */
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-4px); }
    20%, 40%, 60%, 80% { transform: translateX(4px); }
}
.shake {
    animation: shake 0.5s var(--ease-smooth) forwards;
}

/* Progress Bar Fill Animation */
@keyframes progress-fill {
    from { width: 0%; }
    to { width: var(--progress-width); }
}
.progress-animate {
    animation: progress-fill 1s var(--ease-out-expo) forwards;
}

/* Gradient Shimmer for Progress */
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
.progress-shimmer {
    background: linear-gradient(90deg, #4F46E5 0%, #6366F1 50%, #4F46E5 100%);
    background-size: 200% 100%;
    animation: shimmer 2s infinite;
    border-radius: 4px;
}

/* Ripple Effect */
@keyframes ripple {
    0% { transform: scale(0); opacity: 0.5; }
    100% { transform: scale(4); opacity: 0; }
}
.ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.5);
    animation: ripple 0.6s ease-out;
    pointer-events: none;
}

/* Confetti Animation */
@keyframes confetti-fall {
    0% { transform: translateY(-100%) rotate(0deg); opacity: 1; }
    100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
}
.confetti {
    position: fixed;
    width: 10px;
    height: 10px;
    top: -10px;
    animation: confetti-fall 3s linear forwards;
    z-index: 9999;
    pointer-events: none;
}

/* Float Animation for Icons */
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-4px); }
}
.float {
    animation: float 2s var(--ease-smooth) infinite;
}

/* Glow Animation */
@keyframes glow {
    0%, 100% { box-shadow: 0 0 5px rgba(79, 70, 229, 0.3); }
    50% { box-shadow: 0 0 20px rgba(79, 70, 229, 0.6); }
}
.glow {
    animation: glow 2s var(--ease-smooth) infinite;
}

/* Counter Animation */
@keyframes countUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.counter-animate {
    animation: countUp 0.6s var(--ease-out-expo) forwards;
}

/* Accordion Expand Animation */
@keyframes accordion-expand {
    from { max-height: 0; opacity: 0; }
    to { max-height: var(--max-height); opacity: 1; }
}
.accordion-expand {
    animation: accordion-expand 0.3s var(--ease-smooth) forwards;
}

/* Accordion Collapse Animation */
@keyframes accordion-collapse {
    from { max-height: var(--max-height); opacity: 1; }
    to { max-height: 0; opacity: 0; }
}
.accordion-collapse {
    animation: accordion-collapse 0.2s var(--ease-smooth) forwards;
}

/* Tooltip Fade In */
@keyframes tooltip-fade {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
}
.tooltip-animate {
    animation: tooltip-fade 0.2s var(--ease-smooth) forwards;
}

/* Button Press Animation */
@keyframes button-press {
    0% { transform: scale(1); }
    50% { transform: scale(0.97); }
    100% { transform: scale(1); }
}
.button-press {
    animation: button-press 0.15s var(--ease-smooth) forwards;
}

/* Hover Lift Animation */
@keyframes hover-lift {
    0% { transform: translateY(0); box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
    100% { transform: translateY(-4px); box-shadow: 0 12px 24px rgba(0,0,0,0.12); }
}
.hover-lift {
    transition: all 0.3s var(--ease-smooth);
}
.hover-lift:hover {
    animation: hover-lift 0.3s var(--ease-spring) forwards;
}

/* Underline Slide Animation */
@keyframes underline-slide {
    from { width: 0; left: 50%; }
    to { width: 100%; left: 0; }
}
.underline-animate {
    position: relative;
}
.underline-animate::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 50%;
    width: 0;
    height: 2px;
    background: currentColor;
    transition: width 0.3s var(--ease-smooth), left 0.3s var(--ease-smooth);
}
.underline-animate:hover::after {
    width: 100%;
    left: 0;
}

/* Scale In for Modals/Dialogs */
@keyframes scale-in {
    from { opacity: 0; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
}
.scale-in {
    animation: scale-in 0.2s var(--ease-out-expo) forwards;
}

/* Fade Out */
@keyframes fadeOut {
    from { opacity: 1; transform: translateY(0); }
    to { opacity: 0; transform: translateY(-10px); }
}
.fade-out {
    animation: fadeOut 0.3s var(--ease-smooth) forwards;
}
"""

# =============================================================================
# TOAST NOTIFICATION COMPONENT
# =============================================================================

TOAST_CSS = """
/* Toast Container */
.toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10000;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

/* Toast Base Styles */
.toast {
    min-width: 300px;
    max-width: 450px;
    padding: 16px 20px;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    font-weight: 500;
    animation: slideInRight 0.3s var(--ease-out-expo) forwards;
    backdrop-filter: blur(8px);
}

.toast-exit {
    animation: fadeOut 0.3s var(--ease-smooth) forwards;
}

/* Toast Variants */
.toast-success {
    background: rgba(255, 255, 255, 0.95);
    border-left: 4px solid #10B981;
    color: #065F46;
}

.toast-error {
    background: rgba(255, 255, 255, 0.95);
    border-left: 4px solid #EF4444;
    color: #991B1B;
}

.toast-warning {
    background: rgba(255, 255, 255, 0.95);
    border-left: 4px solid #F59E0B;
    color: #92400E;
}

.toast-info {
    background: rgba(255, 255, 255, 0.95);
    border-left: 4px solid #4F46E5;
    color: #312E81;
}

/* Toast Icon */
.toast-icon {
    flex-shrink: 0;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
}

.toast-success .toast-icon {
    background: #D1FAE5;
    color: #059669;
}

.toast-error .toast-icon {
    background: #FEE2E2;
    color: #DC2626;
}

.toast-warning .toast-icon {
    background: #FEF3C7;
    color: #D97706;
}

.toast-info .toast-icon {
    background: #EEF2FF;
    color: #4F46E5;
}

/* Toast Message */
.toast-message {
    flex: 1;
    line-height: 1.5;
}

/* Toast Close Button */
.toast-close {
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px;
    opacity: 0.5;
    transition: opacity 0.2s ease;
    color: inherit;
}

.toast-close:hover {
    opacity: 1;
}

/* Toast Progress Bar */
.toast-progress {
    position: absolute;
    bottom: 0;
    left: 0;
    height: 3px;
    background: rgba(0, 0, 0, 0.1);
    border-radius: 0 0 12px 12px;
    animation: progress-fill 3s linear forwards;
}
"""

TOAST_COMPONENT = """
<div class="toast-container" id="toast-container"></div>

<script>
function showToast(message, type = 'info', duration = 3000) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const icons = {
        success: '✓',
        error: '✕',
        warning: '!',
        info: 'i'
    };

    toast.innerHTML = `
        <div class="toast-icon">${icons[type] || icons.info}</div>
        <div class="toast-message">${message}</div>
        <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
        <div class="toast-progress" style="animation-duration: ${duration}ms"></div>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('toast-exit');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}
</script>
"""


# =============================================================================
# PROGRESS INDICATOR COMPONENT
# =============================================================================

PROGRESS_CSS = """
/* Step Progress Indicator */
.step-progress {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 24px 0;
}

.step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    flex: 1;
    position: relative;
}

.step:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 12px;
    left: 50%;
    width: 100%;
    height: 2px;
    background: #E5E7EB;
    transform: translateX(-50%);
    z-index: 0;
}

.step.completed:not(:last-child)::after {
    background: #4F46E5;
    animation: progress-fill 0.5s var(--ease-smooth) forwards;
}

.step-dot {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    border: 2px solid #E5E7EB;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 600;
    z-index: 1;
    transition: all 0.3s var(--ease-smooth);
}

.step.completed .step-dot {
    background: #4F46E5;
    border-color: #4F46E5;
    color: white;
}

.step.active .step-dot {
    border-color: #4F46E5;
    box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
    animation: pulse 1.5s infinite;
}

.step-label {
    font-size: 12px;
    color: #6B7280;
    font-weight: 500;
    transition: color 0.3s ease;
}

.step.completed .step-label,
.step.active .step-label {
    color: #1A1D23;
}

/* Circular Progress Ring */
.progress-ring {
    position: relative;
    width: 60px;
    height: 60px;
}

.progress-ring-circle {
    fill: none;
    stroke-width: 4;
    stroke-linecap: round;
    transform: rotate(-90deg);
    transform-origin: 50% 50%;
}

.progress-ring-bg {
    stroke: #E5E7EB;
}

.progress-ring-fill {
    stroke: #4F46E5;
    stroke-dasharray: 157;
    stroke-dashoffset: 157;
    transition: stroke-dashoffset 1s var(--ease-smooth);
}

.progress-ring-value {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 14px;
    font-weight: 700;
    color: #1A1D23;
}

/* Linear Progress Bar */
.progress-bar {
    width: 100%;
    height: 8px;
    background: #E5E7EB;
    border-radius: 4px;
    overflow: hidden;
    position: relative;
}

.progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #4F46E5 0%, #6366F1 100%);
    border-radius: 4px;
    transition: width 0.5s var(--ease-smooth);
    position: relative;
}

.progress-bar-fill::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255, 255, 255, 0.3),
        transparent
    );
    animation: shimmer 2s infinite;
}

/* Progress with Percentage */
.progress-with-percent {
    display: flex;
    align-items: center;
    gap: 12px;
}

.progress-percent {
    font-size: 14px;
    font-weight: 600;
    color: #4F46E5;
    min-width: 45px;
    text-align: right;
}
"""


# =============================================================================
# CARD HOVER EFFECTS
# =============================================================================

CARD_HOVER_CSS = """
/* Premium Card with Hover Effects */
.premium-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    margin: 16px 0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04);
    border: 1px solid transparent;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.premium-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 100%;
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.03) 0%, transparent 50%);
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
}

.premium-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12), 0 4px 8px rgba(0, 0, 0, 0.08);
    border-color: rgba(79, 70, 229, 0.15);
}

.premium-card:hover::before {
    opacity: 1;
}

.premium-card:active {
    transform: scale(0.99) translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Card with Left Accent Bar */
.card-accent {
    position: relative;
    padding-left: 28px;
}

.card-accent::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    border-radius: 2px;
    background: #4F46E5;
    transition: width 0.3s ease;
}

.card-accent:hover::before {
    width: 6px;
}

/* Card Glow on Hover */
.card-glow {
    position: relative;
}

.card-glow::after {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: 14px;
    background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%);
    opacity: 0;
    z-index: -1;
    transition: opacity 0.3s ease;
}

.card-glow:hover::after {
    opacity: 0.1;
}

/* Interactive Card */
.card-interactive {
    cursor: pointer;
    user-select: none;
}

.card-interactive .card-arrow {
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    transition: transform 0.3s ease;
    opacity: 0;
}

.card-interactive:hover .card-arrow {
    transform: translateY(-50%) translateX(4px);
    opacity: 1;
}
"""


# =============================================================================
# BUTTON ENHANCEMENTS
# =============================================================================

BUTTON_CSS = """
/* Premium Button Base */
.btn-premium {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 14px 28px;
    font-size: 15px;
    font-weight: 600;
    border-radius: 12px;
    border: none;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

/* Primary Button */
.btn-primary {
    background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%);
    color: white;
    box-shadow: 0 2px 4px rgba(79, 70, 229, 0.15);
}

.btn-primary:hover {
    background: linear-gradient(135deg, #4338CA 0%, #4F46E5 100%);
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(79, 70, 229, 0.25);
}

.btn-primary:active {
    transform: scale(0.98) translateY(0);
    box-shadow: 0 2px 4px rgba(79, 70, 229, 0.15);
}

.btn-primary:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.3);
}

/* Secondary Button */
.btn-secondary {
    background: white;
    color: #4F46E5;
    border: 2px solid #4F46E5;
}

.btn-secondary:hover {
    background: #EEF2FF;
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(79, 70, 229, 0.15);
}

/* Ghost Button */
.btn-ghost {
    background: transparent;
    color: #4F46E5;
}

.btn-ghost:hover {
    background: #EEF2FF;
}

/* Button with Ripple Effect */
.btn-ripple {
    position: relative;
    overflow: hidden;
}

.btn-ripple::after {
    content: '';
    position: absolute;
    width: 100px;
    height: 100px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    transform: scale(0);
    opacity: 0;
    pointer-events: none;
}

.btn-ripple:active::after {
    animation: ripple 0.6s ease-out;
}

/* Loading Button */
.btn-loading {
    pointer-events: none;
    opacity: 0.7;
}

.btn-loading .btn-text {
    opacity: 0;
}

.btn-loading .btn-spinner {
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Icon Button */
.btn-icon {
    width: 40px;
    height: 40px;
    padding: 0;
    border-radius: 10px;
}

.btn-icon:hover {
    transform: scale(1.1);
}
"""


# =============================================================================
# INPUT ENHANCEMENTS
# =============================================================================

INPUT_CSS = """
/* Premium Input */
.input-premium {
    width: 100%;
    padding: 14px 16px;
    font-size: 15px;
    border: 1.5px solid #E5E7EB;
    border-radius: 10px;
    background: white;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    outline: none;
}

.input-premium:hover {
    border-color: #D1D5DB;
}

.input-premium:focus {
    border-color: #4F46E5;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.input-premium::placeholder {
    color: #9CA3AF;
}

/* Input with Icon */
.input-with-icon {
    position: relative;
}

.input-with-icon .input-icon {
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    color: #9CA3AF;
    pointer-events: none;
    transition: color 0.2s ease;
}

.input-with-icon.focused .input-icon {
    color: #4F46E5;
}

.input-with-icon input {
    padding-left: 44px;
}

/* Textarea */
.textarea-premium {
    min-height: 150px;
    resize: vertical;
    line-height: 1.6;
}

/* Input Error State */
.input-error {
    border-color: #EF4444 !important;
    animation: shake 0.5s ease;
}

.input-error:focus {
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1) !important;
}

/* Input Success State */
.input-success {
    border-color: #10B981 !important;
}

.input-success:focus {
    box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1) !important;
}

/* File Upload Zone */
.upload-zone {
    border: 2px dashed #E5E7EB;
    border-radius: 12px;
    padding: 32px;
    text-align: center;
    background: white;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
}

.upload-zone:hover {
    border-color: #4F46E5;
    background: #EEF2FF;
}

.upload-zone.dragover {
    border-color: #4F46E5;
    background: #EEF2FF;
    transform: scale(1.02);
}
"""


# =============================================================================
# TOOLTIP COMPONENT
# =============================================================================

TOOLTIP_CSS = """
/* Tooltip Base */
.tooltip {
    position: relative;
    display: inline-block;
}

.tooltip::before {
    content: attr(data-tooltip);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%) translateY(-8px);
    padding: 8px 12px;
    background: #1A1D23;
    color: white;
    font-size: 13px;
    font-weight: 500;
    border-radius: 8px;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: all 0.2s var(--ease-smooth);
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.tooltip::after {
    content: '';
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%) translateY(-2px);
    border: 6px solid transparent;
    border-top-color: #1A1D23;
    opacity: 0;
    pointer-events: none;
    transition: all 0.2s var(--ease-smooth);
    z-index: 1000;
}

.tooltip:hover::before,
.tooltip:hover::after {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
}

/* Tooltip Positions */
.tooltip-top::before {
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
}

.tooltip-bottom::before {
    top: 100%;
    bottom: auto;
    left: 50%;
    transform: translateX(-50%);
}

.tooltip-left::before {
    right: 100%;
    bottom: 50%;
    left: auto;
    transform: translateY(50%);
}

.tooltip-right::before {
    left: 100%;
    bottom: 50%;
    transform: translateY(50%);
}

/* Tooltip Sizes */
.tooltip-wide::before {
    max-width: 250px;
    white-space: normal;
}
"""


# =============================================================================
# LOADING STATE COMPONENTS
# =============================================================================

def render_loading_spinner(message: str = "Loading") -> str:
    """Render a premium loading spinner with animated dots."""
    return f"""
    <div style="display: flex; flex-direction: column; align-items: center; padding: 40px;">
        <div class="spinner" style="margin-bottom: 24px;"></div>
        <h3 style="color: #1A1D23; font-weight: 600; margin-bottom: 8px;">
            {message}<span class="loading-dots"></span>
        </h3>
        <p style="color: #6B7280; font-size: 14px;">This usually takes 10-20 seconds</p>
    </div>
    """


def render_skeleton_card() -> str:
    """Render a skeleton loading card."""
    return """
    <div class="premium-card" style="animation: fadeIn 0.5s ease;">
        <div class="skeleton" style="height: 24px; width: 60%; margin-bottom: 16px;"></div>
        <div class="skeleton" style="height: 16px; width: 40%; margin-bottom: 12px;"></div>
        <div class="skeleton" style="height: 16px; width: 80%; margin-bottom: 8px;"></div>
        <div style="display: flex; gap: 12px; margin-top: 16px;">
            <div class="skeleton" style="height: 40px; width: 120px;"></div>
            <div class="skeleton" style="height: 40px; width: 100px;"></div>
        </div>
    </div>
    """


def render_skeleton_list(count: int = 3) -> str:
    """Render multiple skeleton cards with staggered animation."""
    cards = []
    for i in range(count):
        cards.append(f"""
        <div class="premium-card" style="animation: fadeIn 0.5s ease {i * 0.1}s both;">
            <div class="skeleton" style="height: 24px; width: 60%; margin-bottom: 16px;"></div>
            <div class="skeleton" style="height: 16px; width: 40%; margin-bottom: 12px;"></div>
            <div class="skeleton" style="height: 16px; width: 80%; margin-bottom: 8px;"></div>
        </div>
        """)
    return "".join(cards)


# =============================================================================
# PROGRESS INDICATOR COMPONENTS
# =============================================================================

def render_step_progress(steps: list, current_step: int) -> str:
    """
    Render a step progress indicator.

    Args:
        steps: List of step labels
        current_step: Current step index (0-based)
    """
    step_html = []
    for i, label in enumerate(steps):
        status_class = ""
        dot_content = str(i + 1)

        if i < current_step:
            status_class = "completed"
            dot_content = "✓"
        elif i == current_step:
            status_class = "active"

        step_html.append(f"""
        <div class="step {status_class}">
            <div class="step-dot">{dot_content}</div>
            <div class="step-label">{label}</div>
        </div>
        """)

    return f'<div class="step-progress">{"".join(step_html)}</div>'


def render_circular_progress(value: int, max_value: int = 100, label: str = "") -> str:
    """
    Render a circular progress ring.

    Args:
        value: Current value
        max_value: Maximum value
        label: Optional label to display in center
    """
    circumference = 2 * 3.14159 * 25  # r = 25
    offset = circumference - (value / max_value) * circumference

    return f"""
    <div class="progress-ring">
        <svg width="60" height="60">
            <circle class="progress-ring-bg" cx="30" cy="30" r="25"></circle>
            <circle class="progress-ring-fill" cx="30" cy="30" r="25"
                    style="stroke-dashoffset: {offset}"></circle>
        </svg>
        <div class="progress-ring-value">{label or value}%</div>
    </div>
    """


def render_linear_progress(value: int, show_percent: bool = True) -> str:
    """
    Render a linear progress bar.

    Args:
        value: Progress percentage (0-100)
        show_percent: Whether to show percentage text
    """
    if show_percent:
        return f"""
        <div class="progress-with-percent">
            <div class="progress-bar" style="flex: 1;">
                <div class="progress-bar-fill" style="width: {value}%;"></div>
            </div>
            <div class="progress-percent">{value}%</div>
        </div>
        """
    return f"""
    <div class="progress-bar">
        <div class="progress-bar-fill" style="width: {value}%;"></div>
    </div>
    """


# =============================================================================
# TOAST NOTIFICATION COMPONENTS
# =============================================================================

def render_toast_container() -> str:
    """Render the toast notification container."""
    return TOAST_COMPONENT


def render_toast(message: str, toast_type: str = "info", auto_close: bool = True) -> str:
    """
    Render a single toast notification.

    Args:
        message: Toast message text
        toast_type: Type of toast (success, error, warning, info)
        auto_close: Whether to auto-close
    """
    icons = {
        "success": "✓",
        "error": "✕",
        "warning": "!",
        "info": "i"
    }

    icon = icons.get(toast_type, icons["info"])

    return f"""
    <div class="toast toast-{toast_type}">
        <div class="toast-icon">{icon}</div>
        <div class="toast-message">{message}</div>
    </div>
    """


# =============================================================================
# UTILITY COMPONENTS
# =============================================================================

def render_counter_animation(end_value: int, duration: int = 1000, prefix: str = "", suffix: str = "") -> str:
    """
    Render an animated counter.

    Args:
        end_value: Final value to count to
        duration: Animation duration in milliseconds
        prefix: Text before the number
        suffix: Text after the number
    """
    return f"""
    <span class="counter-animate"
          data-count-to="{end_value}"
          data-duration="{duration}"
          data-prefix="{prefix}"
          data-suffix="{suffix}">
        {prefix}{end_value}{suffix}
    </span>
    """


def render_badge(text: str, color: str = "#4F46E5") -> str:
    """
    Render a badge/chip component.

    Args:
        text: Badge text
        color: Badge background color
    """
    return f"""
    <span class="skill-chip" style="background: {color}20; color: {color};">
        {text}
    </span>
    """


def render_icon_button(icon: str, tooltip: str = "", color: str = "#4F46E5") -> str:
    """
    Render an icon button with optional tooltip.

    Args:
        icon: Icon character or HTML
        tooltip: Optional tooltip text
        color: Button color
    """
    tooltip_attr = f'data-tooltip="{tooltip}"' if tooltip else ""
    return f"""
    <button class="btn-premium btn-icon tooltip {tooltip_attr}"
            style="background: {color}15; color: {color};">
        {icon}
    </button>
    """


# =============================================================================
# COMPLETE CSS BUNDLE
# =============================================================================

def get_all_css() -> str:
    """Get all CSS for micro-interactions."""
    return f"""
    <style>
    {CSS_ANIMATIONS}
    {TOAST_CSS}
    {PROGRESS_CSS}
    {CARD_HOVER_CSS}
    {BUTTON_CSS}
    {INPUT_CSS}
    {TOOLTIP_CSS}
    </style>
    """


# =============================================================================
# MICRO-COPY LIBRARY
# =============================================================================

MICRO_COPY = {
    # Loading messages
    "loading": {
        "scanning": "Scanning your emails for opportunities",
        "identifying": "Identifying scholarships, internships, and more",
        "extracting": "Extracting deadlines and requirements",
        "matching": "Matching opportunities to your profile",
        "ranking": "Ranking by urgency and fit",
        "preparing": "Preparing your personalized results",
    },

    # Success messages
    "success": {
        "copied": "Copied to clipboard!",
        "applied": "Marked as applied! Great job!",
        "reminder_set": "Reminder set successfully",
        "exported": "Exported successfully",
        "saved": "Saved to your opportunities",
    },

    # Encouragement messages
    "encouragement": [
        "Rolling deadlines often mean earlier applications have better chances!",
        "Pro tip: Save your top 3 opportunities to prioritize your time.",
        "Many scholarships favor applicants with strong personal statements.",
        "Don't forget to request recommendation letters early!",
        "You've got this! One application at a time.",
        "Every application brings you closer to your goals!",
    ],

    # Empty states
    "empty": {
        "no_opportunities": "No opportunities match your current filters. Try adjusting your criteria!",
        "no_documents": "No documents required - that's one less thing to worry about!",
        "no_deadlines": "No deadline pressure - but don't wait too long!",
    },

    # Tooltips
    "tooltips": {
        "match_score": "Based on your degree, CGPA, skills, and preferences",
        "urgency_critical": "Deadline in 3 days or less - act now!",
        "urgency_urgent": "Deadline in 4-7 days - start soon!",
        "urgency_moderate": "Deadline in 8-30 days - plan ahead!",
        "urgency_comfortable": "Deadline in 31+ days - plenty of time!",
        "urgency_rolling": "Rolling basis - earlier is better!",
        "urgency_unknown": "Deadline not specified - verify on portal!",
        "apply_now": "Open application portal in new tab",
        "checklist": "View required documents and steps",
        "dismiss": "Remove this opportunity from your list",
    },

    # Button text
    "buttons": {
        "analyze": "Analyze My Opportunities",
        "analyzing": "Analyzing",
        "apply": "Apply Now",
        "checklist": "See Action Checklist",
        "close": "Close Checklist",
        "back": "Back to Input",
        "export": "Export to PDF",
        "copy": "Copy Link",
        "share": "Share",
        "save": "Save for Later",
        "dismiss": "Dismiss",
        "remind": "Set Reminder",
    },

    # Status messages
    "status": {
        "email_detected": "Email detected",
        "emails_detected": "Emails detected",
        "min_required": "Minimum 5 required",
        "ready": "Ready to analyze!",
        "processing": "Processing...",
        "complete": "Analysis complete!",
    },
}


def get_loading_message(step: int) -> str:
    """Get loading message for processing step."""
    messages = list(MICRO_COPY["loading"].values())
    return messages[min(step, len(messages) - 1)]


def get_encouragement() -> str:
    """Get a random encouragement message."""
    import random
    return random.choice(MICRO_COPY["encouragement"])


def get_tooltip(key: str) -> str:
    """Get tooltip text by key."""
    return MICRO_COPY["tooltips"].get(key, "")
