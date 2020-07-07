const { dest, series, src, parallel } = require('gulp');
const concat = require('gulp-concat');
const sass = require('gulp-sass');
const Ordered = require('ordered-read-streams');
const del = require('del');

sass.compiler = require('node-sass');

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
    'node_modules/jquery/dist/jquery.min.js',
    './semantic/dist/semantic.min.js',
  ])
    .pipe(dest(`${djStaticDir}/js`));
}

/**
 * Combine all js files into one
 */
function scripts() {
  return src([
    './gahd/assets/js/app.js',
  ])
    //.pipe(concat('app.js'))
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
 * Move CSS to 'css' dir
 */
function css() {
  return src([
    './semantic/dist/semantic.min.css',
  ])
    .pipe(dest(`${djStaticDir}/css`));
}

/**
 * Move default Fomantic-UI theme to 'css/themes' dir
 */
function semantic() {
  return src([
    './semantic/dist/themes/default/**/*'
  ])
    .pipe(dest(`${djStaticDir}/css/themes/default`));
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
  parallel(js, scripts, css, scss, facss, fafonts, semantic),
  img
);
