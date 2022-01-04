
            <div class="modal-body">
              <div class="col-md-12"></div>
              <div class="col-md-16">
                <div class="form-group">
                  <label>Job Id</label>
                  <input type="text" name="jobid" class="form-control" readonly/>
                </div>
                <!--<div class="form-group">
                  <label>Job name</label>
                  <input type="text" name="jobname" class="form-control" required="required"/>
                </div>-->
                <div class="form-group">
                  <label>Inputfile/-path (Full path to file or root of path to process)</label>
                  <input type="text" name="inputpath" class="form-control" required="required"/>
                </div>
                <div class="form-group">
                  <label>Outputpath (Root directory for output)</label>
                  <input type="text" name="outputpath" class="form-control" required="required"/>
                </div>
                <div class="form-group">
                  <label>Select script to run</label>
                  <select id="scriptSelect" name="script" class="form-control" required="required" onchange="setArguments(this);" selected>
<?php
$processors_json = file_get_contents("processors.json");
$processors = json_decode($processors_json, true);

foreach ($processors as $processor) { ?>
                    <option value="<?php echo $processor['name']; ?>" data-command="<?php echo $processor['command']; ?>" data-commandarguments="<?php echo implode(',', $processor['arguments']);//addslashes(json_encode($processor['arguments'])); ?>"><?php echo $processor['name']; ?></option>
<?php } ?>
                  </select>
                  <script>
                    function setArguments(sel) {
                        var selectedScript = sel.selectedOptions[0];
                        var command = selectedScript.dataset['command'];
                        var arguments = selectedScript.dataset['commandarguments'].split(",");

                        $('#command').val(command);

                        $('#commandarguments').empty()
                        for (var value of arguments) {
                          $('#commandarguments')
                            .append(`<input type="checkbox" id="${value}" name="arguments[]" value="${value}">`)
                            .append(`<label for="${value}">${value}</label></div>`)
                            .append(`<br>`);
                        }
                    }
                    $("#scriptSelect").prop("selectedIndex", -1);
                  </script>
                  <input type="text" id="command" name="command" class="form-control" readonly/><!-- disabled="true"/> -->
                </div>
                <div class="form-group">
                  <label>Select options for the script</label>
                  <div id="commandarguments" class="form-control"> </div>
                </div>
              </div>  
            </div>

