// Initialize all tooltips
document.querySelectorAll('.tooltip-trigger').forEach(trigger => {
  const tooltipId = trigger.getAttribute('data-target');
  const tooltip = document.getElementById(tooltipId);

  if (!tooltip) return;

  // Create the Popper instance for this specific pair
  const popperInstance = Popper.createPopper(trigger, tooltip, {
    placement: 'top',
    modifiers: [
      { name: 'flip', enabled: false }, // Force it to stay on top
      { name: 'offset', options: { offset: [0, 8] } }
    ],
  });

  // Show logic
  function show() {
    tooltip.style.display = 'block';
    popperInstance.update();
  }

  // Hide logic
  function hide() {
    tooltip.style.display = 'none';
  }

  // Bind events to this specific trigger
  trigger.addEventListener('mouseenter', show);
  trigger.addEventListener('focus', show);
  trigger.addEventListener('mouseleave', hide);
  trigger.addEventListener('blur', hide);
});
