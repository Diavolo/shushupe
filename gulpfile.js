import { dest, series, src, parallel } from 'gulp';
import concat from 'gulp-concat';
import sass from 'gulp-sass';
import * as dartSass from 'sass';
import ordered from 'ordered-read-streams';
import { deleteAsync } from 'del';
import fs from 'fs-extra';
import path from 'path';

const sassCompiler = sass(dartSass);

const djStaticDir = 'shushupe/static';

const filesToDelete = [
  `${djStaticDir}/*`
];

/**
 * Clean files
 */
async function clean() {
  const deletedFilePaths = await deleteAsync(filesToDelete, { force: true });
  deletedFilePaths.forEach((i) => console.log('Deleted', i));
}

/**
 * Move JS files to 'js' dir
 */
async function js() {
  const sourceFile = 'node_modules/alpinejs/dist/alpine.js';
  const targetDir = `${djStaticDir}/js`;
  const targetFile = path.join(targetDir, 'alpine.min.js');

  await fs.ensureDir(targetDir);
  await fs.copy(sourceFile, targetFile);
}

/**
 * Combine scss and css files into one
 */
function scss() {
  let sassStream = src([
    './shushupe/scss/**/*.scss'
  ])
    .pipe(sassCompiler().on('error', sassCompiler.logError));

  let cssStream = src([
    './shushupe/assets/css/pygments.css',
  ]);

  return ordered([sassStream, cssStream])
    .pipe(concat('app.css'))
    .pipe(dest(`${djStaticDir}/css`));
}

/**
 * Move FontAwesome css to 'css' dir
 */
async function facss() {
  const sourceFile = 'node_modules/@fortawesome/fontawesome-free/css/all.min.css';
  const targetDir = `${djStaticDir}/css`;
  const targetFile = path.join(targetDir, 'fontawesome.min.css');

  await fs.ensureDir(targetDir);
  await fs.copy(sourceFile, targetFile);
}

/**
 * Move FontAwesome fonts to 'webfonts' css dir
 */
async function fafonts() {
  const sourceDir = 'node_modules/@fortawesome/fontawesome-free/webfonts';
  const targetDir = `${djStaticDir}/webfonts`;

  await fs.ensureDir(targetDir);
  await fs.copy(sourceDir, targetDir);
}

/**
 * Move Inter UI fonts
 */
async function interUiFonts() {
  const sourceDir = 'node_modules/inter-ui/web';
  const targetDir = `${djStaticDir}/css/web`;

  await fs.ensureDir(targetDir);
  await fs.copy(sourceDir, targetDir);
}

/**
 * Move inter UI css
 */
async function interUiCss() {
  const sourceFile = 'node_modules/inter-ui/inter.css';
  const targetDir = `${djStaticDir}/css`;
  const targetFile = path.join(targetDir, 'inter.css');

  await fs.ensureDir(targetDir);
  await fs.copy(sourceFile, targetFile);
}

/**
 * Move images to 'img' dir
 */
async function img() {
  const sourceDir = './shushupe/assets/img';
  const targetDir = `${djStaticDir}/img`;

  await fs.ensureDir(targetDir);
  await fs.copy(sourceDir, targetDir);
}

export { clean };
export const build = series(
  clean,
  parallel(js, scss, facss, fafonts, interUiFonts, interUiCss),
  img
);
