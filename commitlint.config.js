// CommonJS so @commitlint/load's sync .js loader works on Node 21+ / 26+
// (isDynamicAwaitSupported incorrectly requires minor >= 8, so ESM export
// default is left unwrapped and extends never applies).
module.exports = { extends: ['@commitlint/config-conventional'] };
