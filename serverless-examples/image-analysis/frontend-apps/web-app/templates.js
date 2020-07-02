/* exported  urlListItemTpl, imageListTpl, imageListItemTpl */

'use strict';

// url list item template
// this is not used b/c we want to use displayable url
function urlListItemTpl (item) {
  /*jshint -W101 */
  return `<li class="list-group-item d-flex justify-content-between align-items-center"><a href="#" class="target-url">${item.url}</a><span class="badge badge-primary badge-pill">${item.stat}</span></li>`;
  /*jshint +W101 */
}

// image list template
function imageListTpl (url, list) {
  /*jshint -W101 */
  return `<h4>URL: ${url}</h4>
    <canvas id="word-cloud" width="600px" height="400px" style="width: 600px; height: 400px;"></canvas>
    <div width="600px" height="400px" style="width: 600px; height: 400px; float: right;">
      <canvas id="histogram"  width="600px" height="400px" style="width: 600px; height: 400px;"></canvas>
    </div>
    <div class="list-group">
    ${list}
    </div>`;
  /*jshint +W101 */
}

// image list item template
function imageListItemTpl (bucketRoot, item) {
  let tags = '';
  let imageName = item.image.split('/');
  imageName = imageName[imageName.length - 1];

  item.labels.forEach(label => {
    /*jshint -W101 */
    tags += `<p class="mb-1"><small>${label.Name} (${label.Confidence})</small></p>`;
    /*jshint +W101 */
  });

  /*jshint -W101 */
  return `
    <div href="#" class="list-group-item list-group-item-action flex-column align-items-start">
      <div class="d-flex w-100 justify-content-between">
        <img height="100px" src="${bucketRoot}/${item.image}"/>
        <small>${imageName}</small>
      </div>
      ${tags}
    </div>`;
  /*jshint +W101 */
}


