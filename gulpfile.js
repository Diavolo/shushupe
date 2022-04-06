const { dest, series, src, parallel } = require('gulp');
const concat = require('gulp-concat');
const sass = require('gulp-sass')(require('sass'));
const Ordered = require('ordered-read-streams');
const del = require('del');

const djStaticDir = 'gahd/static';

const filesToDelete = [
  `${djStaticDir}/*`
];

/**
 * Clean files
 */
async function clean() {
  const deletedFilePaths = await del(filesToDelete, { force: true });
  deletedFilePaths.forEach((i) => console.log('Deleted', i));
}

/**
 * Move JS files to 'js' dir
 */
function js() {
  return src([
    'node_modules/alpinejs/dist/cdn.min.js',
  ])
    .pipe(concat('alpine.min.js'))
    .pipe(dest(`${djStaticDir}/js`));
}

/**
 * Combine scss and css files into one
 */
function scss() {
  sassStream = src([
    './gahd/scss/**/*.scss'
  ])
    .pipe(sass().on('error', sass.logError));

  cssStream = src([
    './gahd/assets/css/pygments.css',
  ]);

  return new Ordered([sassStream, cssStream])
    .pipe(concat('app.css'))
    .pipe(dest(`${djStaticDir}/css`));
}

/**
 * Move FontAwesome css to 'css' dir
 */
function facss() {
  return src([
    'node_modules/@fortawesome/fontawesome-free/css/all.min.css',
  ])
    .pipe(concat('fontawesome.min.css'))
    .pipe(dest(`${djStaticDir}/css`));
}

/**
 * Move FontAwesome fonts to 'webfonts' css dir
 */
function fafonts() {
  return src([
    'node_modules/@fortawesome/fontawesome-free/webfonts/*',
  ])
    .pipe(dest(`${djStaticDir}/webfonts`));
}

/**
 * Move Inter UI fonts
 */
function interUiFonts() {
  return src([
    'node_modules/inter-ui/Inter (web)/*'
  ])
    .pipe(dest(`${djStaticDir}/css/Inter (web)`));
}

/**
 * Move inter UI css
 */
function interUiCss() {
  return src([
    'node_modules/inter-ui/inter.css'
  ])
    .pipe(dest(`${djStaticDir}/css`));
}

/**
 * Move images to 'img' dir
 */
function img() {
  return src([
    './gahd/assets/img/*',
  ])
    .pipe(dest(`${djStaticDir}/img`));
}

exports.clean = clean;
exports.build = series(
  clean,
  parallel(js, scss, facss, fafonts, interUiFonts, interUiCss),
  img
);
