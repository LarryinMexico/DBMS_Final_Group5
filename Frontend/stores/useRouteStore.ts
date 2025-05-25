// stores/route.ts
import { defineStore } from "pinia";

export const useRouteStore = defineStore("route", {
  state: () => ({
    destination: null as { lat: number; lng: number } | null,
    routeGeoJSON: null as GeoJSON.FeatureCollection | null,
  }),
  actions: {
    async fetchRoute(
      from: { lat: number; lng: number },
      to: { lat: number; lng: number },
    ) {
      const res = await fetch(
        `https://api.mapbox.com/directions/v5/mapbox/walking/${from.lng},${from.lat};${to.lng},${to.lat}?geometries=geojson&access_token=pk.eyJ1IjoiY2h1YW5nMDkxIiwiYSI6ImNtOTE3NTZldzB2cWYyanNraGh1dGkzdzMifQ.IqUIwZ1dEf7Prbnb4bMeng`,
      );
      const data = await res.json();
      this.routeGeoJSON = {
        type: "FeatureCollection",
        features: [
          {
            type: "Feature",
            properties: {},
            geometry: data.routes[0].geometry,
          },
        ],
      };
      this.destination = to;
    },
    clearRoute() {
      this.routeGeoJSON = null;
      this.destination = null;
    },
  },
});
