from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import IrishCounty, EuropeanCity, TransportationRoute


@admin.register(IrishCounty)
class IrishCountyAdmin(OSMGeoAdmin):
    """Admin interface for Irish counties with map widget"""

    list_display = ['display_name', 'name_en', 'name_ga', 'area_display']
    search_fields = ['name_tag', 'name_en', 'name_ga', 'alt_name']
    list_filter = ['name_en']
    readonly_fields = ['osm_id', 'area', 'latitude', 'longitude', 'area_display', 'display_name']

    # Map widget settings
    default_zoom = 7
    default_lat = 53.41291
    default_lon = -8.24389

    def area_display(self, obj):
        """Display formatted area"""
        if obj.area:
            return f"{obj.area:.0f} units"
        elif obj.geom:
            return f"{obj.area_km2:.0f} km²"
        return "N/A"
    area_display.short_description = "Area"

    def display_name(self, obj):
        """Display the name for list_display and readonly_fields"""
        return obj.name_en  # or customize as needed
    display_name.short_description = "Display Name"


@admin.register(EuropeanCity)
class EuropeanCityAdmin(OSMGeoAdmin):
    """Admin interface for European cities with enhanced features"""

    list_display = ['name', 'country', 'population_formatted', 'population_category', 'coordinates']
    list_filter = ['country']
    search_fields = ['name', 'country']
    readonly_fields = ['latitude', 'longitude', 'population_category', 'coordinates']

    # Map widget settings
    default_zoom = 4
    default_lat = 54.5260
    default_lon = 15.2

    def population_formatted(self, obj):
        """Display formatted population"""
        return f"{obj.population:,}"
    population_formatted.short_description = "Population"
    population_formatted.admin_order_field = 'population'

    def coordinates(self, obj):
        """Display coordinates"""
        if obj.latitude is None or obj.longitude is None:
            return "Unknown"
        return f"({obj.latitude:.4f}, {obj.longitude:.4f})"
    coordinates.short_description = "Coordinates"

    # Custom actions
    actions = ['export_selected_cities']

    def export_selected_cities(self, request, queryset):
        """Export selected cities as CSV"""
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="cities.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Country', 'Population', 'Latitude', 'Longitude'])

        for city in queryset:
            writer.writerow([
                city.name,
                city.country,
                city.population,
                city.latitude,
                city.longitude
            ])

        self.message_user(request, f"Exported {queryset.count()} cities to CSV")
        return response

    export_selected_cities.short_description = "Export selected cities to CSV"


@admin.register(TransportationRoute)
class TransportationRouteAdmin(OSMGeoAdmin):
    """Admin interface for transportation routes"""

    list_display = ['route_name', 'route_type', 'length_display']
    list_filter = ['route_type']
    search_fields = ['route_name']
    readonly_fields = ['length_display']

    # Map widget settings
    default_zoom = 5
    default_lat = 52.0
    default_lon = 5.0

    def length_display(self, obj):
        """Display formatted route length"""
        return f"{obj.length_km:.1f} km"
    length_display.short_description = "Length"
