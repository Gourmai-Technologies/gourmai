module.exports = {
    files: ["gourmai/templates/**/*.html", "gourmai/static/css/**/*.css"],
    reloadDelay: 1, // Delay in milliseconds to reload the browser after changes
    proxy: "localhost:5000", // Flask server address
    open: false // Don't open browser automatically
};

// Install // npm install -g browser-sync
// Run in terminal: browser-sync start --config bs-config.js // Refreshes when files determined above change //
// Run on server // http://localhost:3000
