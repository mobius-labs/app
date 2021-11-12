module.exports = {
    publicPath: "/",
    // change the app's default title (before we override it for specific pages)
    chainWebpack: (config) => {
        config.plugin("html").tap((args) => {
            args[0].title = "Möbius";
            return args;
        });
    },
};
