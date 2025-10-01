from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse

from src.app.domains.earthquake_service import EarthquakeService
from src.app.domains.visualization.schema import EarthquakeMapPoint, EarthquakeMapResponse

visualization_router = APIRouter(prefix="/visualization", tags=["visualization"])


@visualization_router.get("/map", response_model=EarthquakeMapResponse)
def get_earthquake_map_data(
    request: Request,
    start_time: str = Query(description="Start time in YYYY-MM-DD format"),
    end_time: str = Query(description="End time in YYYY-MM-DD format"),
    min_magnitude: float = Query(default=0.0, description="Minimum magnitude filter"),
    max_magnitude: float = Query(default=10.0, description="Maximum magnitude filter"),
    fetch_new_data: bool = Query(default=True, description="Whether to fetch new data from USGS API"),
):
    """
    Get earthquake data optimized for map visualization.

    Args:
        request: FastAPI request object
        start_time: Start date in YYYY-MM-DD format
        end_time: End date in YYYY-MM-DD format
        min_magnitude: Minimum magnitude to include
        max_magnitude: Maximum magnitude to include
        fetch_new_data: Whether to fetch new data from USGS API or use existing database data

    Returns:
        JSON response with earthquake data optimized for mapping
    """
    earthquake_service = EarthquakeService(request)
    map_points = earthquake_service.get_earthquake_data(
        start_time=start_time, end_time=end_time, response_model=EarthquakeMapPoint, fetch_new_data=fetch_new_data
    )

    filtered_map_points = [
        point
        for point in map_points
        if (
            point.latitude is not None
            and point.longitude is not None
            and point.mag is not None
            and min_magnitude <= point.mag <= max_magnitude
        )
    ]

    return EarthquakeMapResponse(
        earthquakes=filtered_map_points,
        total_count=len(filtered_map_points),
        date_range={"start": start_time, "end": end_time},
    )


@visualization_router.get("/map-view", response_class=HTMLResponse)
def get_earthquake_map_view(request: Request):
    """
    Serve the interactive earthquake map visualization page.

    Returns:
        HTML page with interactive map
    """
    request.state.metadata_id = None
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Earthquake Map Visualization</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f5f5f5;
            }
            
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1rem 2rem;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .header h1 {
                margin: 0;
                font-size: 2rem;
                font-weight: 300;
            }
            
            .controls {
                background: white;
                padding: 1rem 2rem;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                display: flex;
                gap: 1rem;
                align-items: center;
                flex-wrap: wrap;
            }
            
            .control-group {
                display: flex;
                flex-direction: column;
                gap: 0.25rem;
            }
            
            .control-group label {
                font-size: 0.9rem;
                font-weight: 500;
                color: #555;
            }
            
            .control-group input, .control-group select {
                padding: 0.5rem;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 0.9rem;
            }
            
            .btn {
                background: #667eea;
                color: white;
                border: none;
                padding: 0.75rem 1.5rem;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.9rem;
                transition: background-color 0.3s;
            }
            
            .btn:hover {
                background: #5a6fd8;
            }
            
            .btn:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            
            .stats {
                background: white;
                padding: 1rem 2rem;
                margin: 0 2rem;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                display: flex;
                gap: 2rem;
                flex-wrap: wrap;
            }
            
            .stat-item {
                text-align: center;
            }
            
            .stat-value {
                font-size: 1.5rem;
                font-weight: bold;
                color: #667eea;
            }
            
            .stat-label {
                font-size: 0.9rem;
                color: #666;
            }
            
            #map {
                height: calc(100vh - 200px);
                margin: 1rem 2rem;
                border-radius: 8px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            
            .loading {
                text-align: center;
                padding: 2rem;
                color: #666;
            }
            
            .error {
                background: #ffebee;
                color: #c62828;
                padding: 1rem;
                margin: 1rem 2rem;
                border-radius: 4px;
                border-left: 4px solid #c62828;
            }
            
            .legend {
                background: white;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                margin: 1rem 2rem;
            }
            
            .legend h3 {
                margin: 0 0 1rem 0;
                color: #333;
            }
            
            .legend-item {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin: 0.5rem 0;
            }
            
            .legend-color {
                width: 20px;
                height: 20px;
                border-radius: 50%;
                border: 2px solid #333;
            }
            
            .data-source-indicator {
                background: #e3f2fd;
                color: #1976d2;
                padding: 0.5rem 1rem;
                border-radius: 4px;
                font-weight: 500;
                border-left: 4px solid #1976d2;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌍 Earthquake Map Visualization</h1>
        </div>
        
        <div class="controls">
            <div class="control-group">
                <label for="startDate">Start Date</label>
                <input type="date" id="startDate" value="2024-01-01">
            </div>
            
            <div class="control-group">
                <label for="endDate">End Date</label>
                <input type="date" id="endDate" value="2024-01-31">
            </div>
            
            <div class="control-group">
                <label for="minMag">Min Magnitude</label>
                <input type="number" id="minMag" value="0" min="0" max="10" step="0.1">
            </div>
            
            <div class="control-group">
                <label for="maxMag">Max Magnitude</label>
                <input type="number" id="maxMag" value="10" min="0" max="10" step="0.1">
            </div>
            
            <div class="control-group">
                <label for="fetchNewData">Data Source</label>
                <select id="fetchNewData">
                    <option value="true">Fetch New Data (USGS API)</option>
                    <option value="false">Use Database Data</option>
                </select>
            </div>
            
            <button class="btn" onclick="loadEarthquakeData()">Load Earthquakes</button>
        </div>
        
        <div class="stats" id="stats" style="display: none;">
            <div class="stat-item">
                <div class="stat-value" id="totalCount">0</div>
                <div class="stat-label">Total Earthquakes</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="maxMagnitude">0</div>
                <div class="stat-label">Max Magnitude</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="dateRange">-</div>
                <div class="stat-label">Date Range</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="dataSource">-</div>
                <div class="stat-label">Data Source</div>
            </div>
        </div>
        
        <div class="legend">
            <h3>Magnitude Legend</h3>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #4CAF50;"></div>
                <span>0.0 - 2.0 (Minor)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #8BC34A;"></div>
                <span>2.0 - 4.0 (Light)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #FFC107;"></div>
                <span>4.0 - 6.0 (Moderate)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #FF9800;"></div>
                <span>6.0 - 8.0 (Strong)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #F44336;"></div>
                <span>8.0+ (Great)</span>
            </div>
        </div>
        
        <div id="map"></div>
        
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            let map;
            let earthquakeMarkers = [];
            
            // Initialize map
            function initMap() {
                map = L.map('map').setView([20, 0], 2);
                
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors'
                }).addTo(map);
            }
            
            // Get color based on magnitude
            function getMagnitudeColor(mag) {
                // Convert to number to ensure proper comparison
                const magnitude = parseFloat(mag) || 0;
                
                if (magnitude >= 8.0) return '#F44336'; // Red - Great
                if (magnitude >= 6.0) return '#FF9800'; // Orange - Strong
                if (magnitude >= 4.0) return '#FFC107'; // Yellow - Moderate
                if (magnitude >= 2.0) return '#8BC34A'; // Light Green - Light
                return '#4CAF50'; // Green - Minor
            }
            
            // Get marker size based on magnitude
            function getMarkerSize(mag) {
                const magnitude = parseFloat(mag) || 0;
                return Math.max(8, Math.min(25, magnitude * 3));
            }
            
            // Clear existing markers
            function clearMarkers() {
                earthquakeMarkers.forEach(marker => map.removeLayer(marker));
                earthquakeMarkers = [];
            }
            
            // Load earthquake data
            async function loadEarthquakeData() {
                const startDate = document.getElementById('startDate').value;
                const endDate = document.getElementById('endDate').value;
                const minMag = document.getElementById('minMag').value;
                const maxMag = document.getElementById('maxMag').value;
                const fetchNewData = document.getElementById('fetchNewData').value;
                
                if (!startDate || !endDate) {
                    alert('Please select both start and end dates');
                    return;
                }
                
                const button = document.querySelector('.btn');
                button.disabled = true;
                button.textContent = fetchNewData === 'true' ? 'Fetching New Data...' : 'Loading from Database...';
                
                let response;
                try {
                    response = await fetch(`/visualization/map?start_time=${startDate}&end_time=${endDate}&min_magnitude=${minMag}&max_magnitude=${maxMag}&fetch_new_data=${fetchNewData}`);
                    
                    if (!response.ok) {
                        // Try to get error details from response
                        let errorMessage = `HTTP error! status: ${response.status}`;
                        try {
                            const errorData = await response.json();
                            if (errorData.detail) {
                                errorMessage = errorData.detail;
                            }
                        } catch {
                            // If we can't parse the error response, use the default message
                        }
                        throw new Error(errorMessage);
                    }
                    
                    const data = await response.json();
                    console.log('Received earthquake data:', data);
                    console.log('First few earthquakes:', data.earthquakes.slice(0, 3));
                    
                    // Clear existing markers
                    clearMarkers();
                    
                    // Add new markers
                    data.earthquakes.forEach(earthquake => {
                        const color = getMagnitudeColor(earthquake.mag || 0);
                        const size = getMarkerSize(earthquake.mag || 0);
                        
                        const marker = L.circleMarker([earthquake.latitude, earthquake.longitude], {
                            radius: size,
                            fillColor: color,
                            color: '#333',
                            weight: 1,
                            opacity: 1,
                            fillOpacity: 0.7
                        });
                        
                        const popupContent = `
                            <div style="min-width: 200px;">
                                <h3 style="margin: 0 0 10px 0; color: #333;">${earthquake.place || 'Unknown Location'}</h3>
                                <p style="margin: 5px 0;"><strong>Magnitude:</strong> ${earthquake.mag || 'N/A'}</p>
                                <p style="margin: 5px 0;"><strong>Time:</strong> ${earthquake.time ? new Date(earthquake.time).toLocaleString() : 'N/A'}</p>
                                <p style="margin: 5px 0;"><strong>Depth:</strong> ${earthquake.depth ? earthquake.depth + ' km' : 'N/A'}</p>
                                <p style="margin: 5px 0;"><strong>Coordinates:</strong> ${earthquake.latitude.toFixed(4)}, ${earthquake.longitude.toFixed(4)}</p>
                                ${earthquake.tsunami ? '<p style="margin: 5px 0; color: #F44336;"><strong>⚠️ Tsunami Alert</strong></p>' : ''}
                                ${earthquake.alert ? `<p style="margin: 5px 0; color: #FF9800;"><strong>Alert:</strong> ${earthquake.alert}</p>` : ''}
                            </div>
                        `;
                        
                        marker.bindPopup(popupContent);
                        marker.addTo(map);
                        earthquakeMarkers.push(marker);
                    });
                    
                    // Update stats
                    updateStats(data);
                    
                    // Fit map to show all markers
                    if (data.earthquakes.length > 0) {
                        const group = new L.featureGroup(earthquakeMarkers);
                        map.fitBounds(group.getBounds().pad(0.1));
                    }
                    
                } catch (error) {
                    console.error('Error loading earthquake data:', error);
                    alert('Error: ' + error.message);
                } finally {
                    button.disabled = false;
                    button.textContent = 'Load Earthquakes';
                }
            }
            
            // Update statistics
            function updateStats(data) {
                const statsDiv = document.getElementById('stats');
                const totalCount = document.getElementById('totalCount');
                const maxMagnitude = document.getElementById('maxMagnitude');
                const dateRange = document.getElementById('dateRange');
                const dataSource = document.getElementById('dataSource');
                
                totalCount.textContent = data.total_count;
                
                const maxMag = Math.max(...data.earthquakes.map(e => e.mag || 0));
                maxMagnitude.textContent = maxMag.toFixed(1);
                
                dateRange.textContent = `${data.date_range.start} to ${data.date_range.end}`;
                
                const fetchNewData = document.getElementById('fetchNewData').value;
                dataSource.textContent = fetchNewData === 'true' ? 'USGS API' : 'Database';
                
                statsDiv.style.display = 'flex';
            }
            
            // Initialize map when page loads
            document.addEventListener('DOMContentLoaded', function() {
                initMap();
                
                // Set default dates (last 30 days)
                const today = new Date();
                const thirtyDaysAgo = new Date(today.getTime() - (30 * 24 * 60 * 60 * 1000));
                
                document.getElementById('endDate').value = today.toISOString().split('T')[0];
                document.getElementById('startDate').value = thirtyDaysAgo.toISOString().split('T')[0];
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
