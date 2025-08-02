document.addEventListener('DOMContentLoaded', () => {
    const levelSelect = document.getElementById('level-select');
    const nameSelect = document.getElementById('name-select');
    const graphContainer = document.getElementById('graph-container');
    const heatmapButton = document.getElementById('show-heatmap');

    function loadGraph(level, name) {
        fetch(`/visualize?level=${level}&name=${name}`)
            .then(response => response.json())
            .then(data => {
                graphContainer.innerHTML = data.graph;
            });
    }

    levelSelect.addEventListener('change', () => {
        const selectedLevel = levelSelect.value;
        const defaultName = selectedLevel === 'country' ? 'World' : 'Mumbai'; // Default options
        loadGraph(selectedLevel, defaultName);
    });

    nameSelect.addEventListener('change', () => {
        const selectedLevel = levelSelect.value;
        const selectedName = nameSelect.value;
        loadGraph(selectedLevel, selectedName);
    });

    heatmapButton.addEventListener('click', () => {
        fetch('/heatmap')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    graphContainer.innerHTML = data.graph;
                }
            });
    });

    // Initialize default graph
    loadGraph('country', 'World');
});
