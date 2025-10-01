# Assumptions & Limitations

This document outlines the key assumptions and limitations of the Earthquake API service.

## Limitations

### API Constraints

#### USGS API Limitations
- **Result Limit**: USGS API has a maximum limit of 20,000 results per request
- **Date Range Impact**: Large date ranges (e.g., months or years) may exceed the result limit
- **No Pagination**: USGS API doesn't provide built-in pagination for large datasets
- **Rate Limiting**: Subject to USGS API rate limiting policies

#### Data Processing Limitations
- **Memory Usage**: Large datasets may impact memory usage during processing
- **Processing Time**: Large date ranges require longer processing times
- **Database Storage**: Accumulated data over time may require database maintenance
- **Real-time Dependency**: Service depends on USGS API availability and performance

### Technical Constraints

#### Performance
- **Synchronous Processing**: ETL operations are synchronous and block API responses
- **No Caching**: No built-in caching mechanism for frequently requested data
- **Single-threaded**: Database operations are not optimized for concurrent access

### User Experience Limitations
- **Error Messages**: Limited error handling for edge cases
- **Data Freshness**: No automatic data refresh mechanism
- **Historical Data**: Limited to USGS API data availability

## Assumptions

### Data Assumptions
- **Fresh Data Preference**: Users always want the most recent data from USGS API
- **Data Completeness**: USGS API data is complete for the requested time ranges
- **Standard Formats**: USGS API maintains consistent data formats over time

### User Behavior Assumptions
- **API Knowledge**: Users are familiar with REST API concepts
- **Error Handling**: Users can interpret and respond to API error messages

### Technical Assumptions
- **Environment Setup**: Users have Docker and Python properly installed
- **Network Connectivity**: Stable internet connection for USGS API access
- **Database Persistence**: PostgreSQL container data persists between restarts
- **Resource Availability**: Sufficient system resources for Docker containers

### Operational Assumptions
- **USGS API Availability**: USGS API is consistently available and responsive
- **Data Consistency**: USGS API maintains consistent data structure
- **Error Recovery**: Network or API errors are temporary and recoverable
- **Database Integrity**: Database migrations run successfully without conflicts
