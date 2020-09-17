module.exports = {
  purge: {
    enabled: false,
    content: [
      './**/*.html',
      './_site/*.html',
      './_site/**/*.html',
    ],
  },
  theme: {
    extend: {}
  },
  variants: {
    borderColor: ['group-hover', 'hover'],
  },
  plugins: [],
}
