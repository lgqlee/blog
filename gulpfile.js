var gulp = require('gulp');
var less = require('gulp-less');
var rename = require("gulp-rename");
var prettify = require('gulp-jsbeautifier');

gulp.task('default', function() {
  console.log("Hello Blog");
});

gulp.task('build-less', function() {
  gulp.src('./resources/assets/css/*/style.less')
    .pipe(less({
      compress: true
    }))
    .on('error', function(e) {
      console.log(e);
    })
    .pipe(prettify({
      indentSize: 2
    }))
    .pipe(rename(function(path) {
      path.basename = path.dirname;
      path.dirname = '';
    }))
    .pipe(gulp.dest('./resources/assets/css/'));
});

gulp.task('watch', ['build-less'], function() {
  gulp.watch([
    './resources/assets/css/**/*.less',
    './resources/assets/css/**/*.variables',
    './resources/assets/css/**/*.overrides'
  ], ['build-less']);
});
