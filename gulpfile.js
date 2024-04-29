const { dest, series, src, parallel } = require('gulp');
const concat = require('gulp-concat');
const sass = require('gulp-sass')(require('sass'));
const Ordered = require('ordered-read-streams');
const del = require('del');

const djStaticDir = 'shushupe/static';

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
    'node_modules/alpinejs/dist/alpine.js',
  ])
    .pipe(concat('alpine.min.js'))
    .pipe(dest(`${djStaticDir}/js`));
}

/**
 * Combine scss and css files into one
 */
function scss() {
  let sassStream = src([
    './shushupe/scss/**/*.scss'
  ])
    .pipe(sass().on('error', sass.logError));

  let cssStream = src([
    './shushupe/assets/css/pygments.css',
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
    'node_modules/inter-ui/web/*',
    'node_modules/inter-ui/web-latin/*'
  ])
    .pipe(dest(`${djStaticDir}/css/web`));
}

/**
 * Move inter UI css
 */
function interUiCss() {
  return src([
    'node_modules/inter-ui/inter.css',
    'node_modules/inter-ui/inter-latin.css'
  ])
    .pipe(dest(`${djStaticDir}/css`));
}

/**
 * Move images to 'img' dir
 */
function img() {
  return src([
    './shushupe/assets/img/*',
  ])
    .pipe(dest(`${djStaticDir}/img`));
}

exports.clean = clean;
exports.build = series(
  clean,
  parallel(js, scss, facss, fafonts, interUiFonts, interUiCss),
  img
);
