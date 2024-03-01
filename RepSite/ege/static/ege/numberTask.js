function createTableForString(str, index) {
      const table = document.createElement('table');
      const indexRow = table.insertRow();
      const charRow = table.insertRow();

      for (let i = 1; i <= str.length; i++) {
        const indexCell = indexRow.insertCell();
        indexCell.textContent = `${i}`;

        const charCell = charRow.insertCell();
        charCell.textContent = str[i-1];
      }

      const tablesContainer = document.getElementById('tablesContainer');
      tablesContainer.appendChild(table);
    }
function numberTask() {
    const strings = ['ege', 'loves']
    for (let i = 0; i < strings.length; i++) {
      createTableForString(strings[i], i);
    }
    }