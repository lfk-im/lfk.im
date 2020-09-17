module.exports = {
  purge: {
    enabled: true,
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
