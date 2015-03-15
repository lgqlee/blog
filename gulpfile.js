/**
 *
 * @authors Vincent Ting (homerdd@gmail.com)
 * @date    2015-03-15 10:47:16
 */

var gulp = require('gulp');
var gutil = require('gulp-util');
var del = require('del');
var less = require('gulp-less');
var rename = require("gulp-rename");
var prettify = require('gulp-jsbeautifier');
var coffee = require('gulp-coffee');
var git = require('gulp-git');

gulp.task('default', function() {
  gutil.log("Hello Blog");
});

// 从 git 上获取 semantic 的文件并放入对应文件夹
gulp.task('setup', function() {
  gutil.log("start clone semantic from github.");
  return git.clone('https://github.com/Semantic-Org/Semantic-UI.git', {
    quite: false
  }, function(err) {
    if (err) {
      return gutil.log(err);
    }
    gutil.log("setup will finish soon.");

    var srcPath = 'Semantic-UI/src/';
    setTimeout(function() {
      del(['Semantic-UI'], function(err, paths) {
        gutil.log('delete folders', paths.join('\n'));
      });
    }, 1500);
    return gulp.src([
        srcPath + '**/*.less',
        srcPath + '!(_site)/**/*.overrides',
        srcPath + '!(_site)/**/*.variables'
      ])
      .pipe(gulp.dest('resources/semantic'));
  });
});

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
