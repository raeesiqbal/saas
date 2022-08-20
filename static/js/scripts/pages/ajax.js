// use of get request
$.ajax({
  type: "get",
  url: `/product-data/${product_id}`,
  dataType: "json",
  success: function (data) {},
  error: (err) => {},
  cache: false,
  contentType: false,
  processData: false,
});
