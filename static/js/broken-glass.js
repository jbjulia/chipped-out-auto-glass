document.addEventListener("DOMContentLoaded", function () {
    /**
     * Gets the canvas element and its context
     */
    const canvas = document.getElementById("brokenGlassCanvas");
    const ctx = canvas.getContext("2d");

    /**
     * Resize canvas to fit window
     */
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    /**
     * Draws a crack on the canvas
     * @param {number} x - The x coordinate of the starting point
     * @param {number} y - The y coordinate of the starting point
     * @param {number} length - The length of the crack
     * @param {number} angle - The angle of the crack
     * @param {number} depth - The recursive depth for drawing child cracks
     */
    function drawCrack(x, y, length, angle, depth) {
        if (depth === 0) return;

        const x2 = x + length * Math.cos(angle);
        const y2 = y + length * Math.sin(angle);

        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x2, y2);
        ctx.stroke();

        const children = Math.floor(Math.random() * 4) + 1; // More children for more branching

        for (let i = 0; i < children; i++) {
            const newLength = length * (0.4 + Math.random() * 0.6);
            const newAngle = angle + (Math.random() - 0.5) * Math.PI / 1.5;
            drawCrack(x2, y2, newLength, newAngle, depth - 1);
        }
    }

    /**
     * Draws chips on the canvas
     * @param {number} x - The x coordinate of the chip center
     * @param {number} y - The y coordinate of the chip center
     * @param {number} num - The number of chips to draw
     */
    function drawChips(x, y, num) {
        for (let i = 0; i < num; i++) {
            const angle = Math.random() * Math.PI * 2;
            const distance = Math.random() * 10;
            const size = Math.random() * 5 + 1;

            ctx.beginPath();
            ctx.arc(x + distance * Math.cos(angle), y + distance * Math.sin(angle), size, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    /**
     * Draws the broken glass effect on the entire canvas
     */
    function drawBrokenGlass() {
        resizeCanvas();
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = "rgba(173, 216, 230, 0.5)";  // Updated to rgba for translucency
        ctx.fillStyle = "rgba(173, 216, 230, 0.5)";  // Updated to rgba for translucency
        ctx.lineWidth = 1;  // Reduced from 2 to 1 for thinner lines

        for (let i = 0; i < 10; i++) {
            const x = Math.random() * canvas.width;
            const y = Math.random() * canvas.height;
            const length = 50 + Math.random() * 50;
            const angle = Math.random() * Math.PI * 2;
            drawCrack(x, y, length, angle, 4);  // Increased depth to 4 for more complex cracks
            drawChips(x, y, Math.floor(Math.random() * 5) + 1);
        }
    }

    drawBrokenGlass();

    setTimeout(() => {
        document.getElementById("brokenGlassContainer").style.opacity = "0";
    }, 10000);
});
