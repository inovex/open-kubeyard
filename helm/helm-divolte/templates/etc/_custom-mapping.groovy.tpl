mapping {
  map timestamp() onto 'timestamp'
  map remoteHost() onto 'remoteHost'
  map eventType() onto 'eventType'
  map location() onto 'location'
  map referer() onto 'referer'
  map partyId() onto 'partyId'
  map sessionId() onto 'sessionId'
  map pageViewId() onto 'pageViewId'

  def locationUri = parse location() to uri
  def localUri = parse locationUri.rawFragment() to uri
  def locationQuery = locationUri.query()
  
  map locationUri.host() onto 'host'
  map localUri.path() onto 'localPath'
  map locationUri.decodedQueryString() onto 'queryString' 
  map locationQuery onto 'queryMap'

  // Map the custom event parameters
  map eventParameters() onto 'paramMap'
  
  def xClientIp = header('X-Client-IP').first()
  map xClientIp onto 'xClientIp'

  // IP-Geo-Mapping
  section {
    def geo = ip2geo(xClientIp)

    map geo.cityId() onto 'cityId'
    map geo.cityName() onto 'cityName'
    map geo.continentCode() onto 'continentCode'
    map geo.continentId() onto 'continentId'
    map geo.continentName() onto 'continentName'
    map geo.countryCode() onto 'countryCode'
    map geo.countryId() onto 'countryId'
    map geo.countryName() onto 'countryName'
    map geo.latitude() onto 'latitude'
    map geo.longitude() onto 'longitude'
    map geo.metroCode() onto 'metroCode'
    map geo.timeZone() onto 'timeZone'
    map geo.mostSpecificSubdivisionCode() onto 'mostSpecificSubdivisionCode'
    map geo.mostSpecificSubdivisionId() onto 'mostSpecificSubdivisionId'
    map geo.mostSpecificSubdivisionName() onto 'mostSpecificSubdivisionName'
    map geo.postalCode() onto 'postalCode'
  }
}