/**
 *
 * @authors Vincent Ting (homerdd@gmail.com)
 * @date    2015-03-15 10:47:16
 */

var gulp = require('gulp');
var gutil = require('gulp-util');
var less = require('gulp-less');
var rename = require("gulp-rename");
var prettify = require('gulp-jsbeautifier');
var coffee = require('gulp-coffee');

gulp.task('default', function() {
  gutil.log("Hello Blog");
});

// todo 考虑将 semantic 从项目中去掉，通过 gulp setup 来进行初始化时下载
// 从而可以默认下载最新版本

// 对 resources 中的 less 文件进行编译
gulp.task('build-less', function() {
  return gulp.src('./resources/assets/less/*/style.less')
    .pipe(less({
      compress: true
    }))
    .on('error', gutil.log)
    .pipe(prettify({
      indentSize: 2
    }))
    .pipe(rename(function(path) {
      path.basename = path.dirname;
      path.dirname = '';
    }))
    .pipe(gulp.dest('./static/css/'));
});

// 对 resources 中的 coffee 文件进行编译
gulp.task('build-coffee', function() {
  return gulp.src('./resources/assets/coffee/**/*.coffee')
    .pipe(coffee({
      bare: true
    }))
    .on('error', gutil.log)
    .pipe(gulp.dest('./static/javascript'));
});

// watch 任务，负责监听 less 和 coffee 文件，并实时编译
gulp.task('watch', ['build-less', 'build-coffee'], function() {
  gulp.watch(['./resources/assets/less/**/*.less',
    './resources/assets/less/**/*.variables',
    './resources/assets/less/**/*.overrides'
  ], ['build-less']);
  gulp.watch([
    './resources/assets/coffee/**/*.coffee'
  ], ['build-coffee']);
});
