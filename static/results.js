var checkboxSelection = function (params) {
    // we put checkbox on the name if we are not doing grouping
    return params.columnApi.getRowGroupColumns().length === 0;
  };
  var headerCheckboxSelection = function (params) {
    // we put checkbox on the name if we are not doing grouping
    return params.columnApi.getRowGroupColumns().length === 0;
  };
  const columnDefs = [
// TODO: fill in 
  ];

  const gridOptions = {
    suppressRowClickSelection: true,
    groupSelectsChildren: true,
    // debug: true,
    rowSelection: 'multiple',
    rowGroupPanelShow: 'always',
    pivotPanelShow: 'always',
    columnDefs: columnDefs,
    pagination: true,
    autoGroupColumnDef: autoGroupColumnDef,
  };
  
  // setup the grid after the page has finished loading
  document.addEventListener('DOMContentLoaded', function () {
    var gridDiv = document.querySelector(''); //TODO: fill in 
    new agGrid.Grid(gridDiv, gridOptions);
  
    fetch()
      .then((response) => response.json())
      .then((data) => gridOptions.api.setRowData(data));
  });