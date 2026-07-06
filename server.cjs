var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
  // If the importer is in node compatibility mode or this is not an ESM
  // file that has been converted to a CommonJS file using a Babel-
  // compatible transform (i.e. "__esModule" has not been set), then set
  // "default" to the CommonJS "module.exports" for node compatibility.
  isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
  mod
));

// server.ts
var import_express = __toESM(require("express"), 1);
var import_path = __toESM(require("path"), 1);
var import_vite = require("vite");
var turf = __toESM(require("@turf/turf"), 1);
var import_compression = __toESM(require("compression"), 1);
var muniNameMap = { "\u10DB\u10EA\u10EE\u10D4\u10D7\u10D8\u10E1": "\u10DB\u10EA\u10EE\u10D4\u10D7\u10D0", "\u10D0\u10EE\u10DB\u10D4\u10E2\u10D8\u10E1": "\u10D0\u10EE\u10DB\u10D4\u10E2\u10D0", "\u10D7\u10D4\u10DA\u10D0\u10D5\u10D8\u10E1": "\u10D7\u10D4\u10DA\u10D0\u10D5\u10D8", "\u10D2\u10E3\u10E0\u10EF\u10D0\u10D0\u10DC\u10D8\u10E1": "\u10D2\u10E3\u10E0\u10EF\u10D0\u10D0\u10DC\u10D8", "\u10E7\u10D5\u10D0\u10E0\u10DA\u10D8\u10E1": "\u10E7\u10D5\u10D0\u10E0\u10D4\u10DA\u10D8", "\u10E1\u10D8\u10E6\u10DC\u10D0\u10E6\u10D8\u10E1": "\u10E1\u10D8\u10E6\u10DC\u10D0\u10E6\u10D8", "\u10D3\u10D4\u10D3\u10DD\u10E4\u10DA\u10D8\u10E1\u10EC\u10E7\u10D0\u10E0\u10DD\u10E1": "\u10D3\u10D4\u10D3\u10DD\u10E4\u10DA\u10D8\u10E1\u10EC\u10E7\u10D0\u10E0\u10DD", "\u10DA\u10D0\u10D2\u10DD\u10D3\u10D4\u10EE\u10D8\u10E1": "\u10DA\u10D0\u10D2\u10DD\u10D3\u10D4\u10EE\u10D8", "\u10E1\u10D0\u10D2\u10D0\u10E0\u10D4\u10EF\u10DD\u10E1": "\u10E1\u10D0\u10D2\u10D0\u10E0\u10D4\u10EF\u10DD", "\u10D7\u10D8\u10D0\u10DC\u10D4\u10D7\u10D8\u10E1": "\u10D7\u10D8\u10D0\u10DC\u10D4\u10D7\u10D8", "\u10D3\u10E3\u10E8\u10D4\u10D7\u10D8\u10E1": "\u10D3\u10E3\u10E8\u10D4\u10D7\u10D8", "\u10E7\u10D0\u10D6\u10D1\u10D4\u10D2\u10D8\u10E1": "\u10E7\u10D0\u10D6\u10D1\u10D4\u10D2\u10D8", "\u10D9\u10D0\u10E1\u10DE\u10D8\u10E1": "\u10D9\u10D0\u10E1\u10DE\u10D8", "\u10D2\u10DD\u10E0\u10D8\u10E1": "\u10D2\u10DD\u10E0\u10D8", "\u10E5\u10D0\u10E0\u10D4\u10DA\u10D8\u10E1": "\u10E5\u10D0\u10E0\u10D4\u10DA\u10D8", "\u10EE\u10D0\u10E8\u10E3\u10E0\u10D8\u10E1": "\u10EE\u10D0\u10E8\u10E3\u10E0\u10D8", "\u10D1\u10DD\u10E0\u10EF\u10DD\u10DB\u10D8\u10E1": "\u10D1\u10DD\u10E0\u10EF\u10DD\u10DB\u10D8", "\u10D0\u10EE\u10D0\u10DA\u10EA\u10D8\u10EE\u10D8\u10E1": "\u10D0\u10EE\u10D0\u10DA\u10EA\u10D8\u10EE\u10D4", "\u10D0\u10D3\u10D8\u10D2\u10D4\u10DC\u10D8\u10E1": "\u10D0\u10D3\u10D8\u10D2\u10D4\u10DC\u10D8", "\u10D0\u10E1\u10DE\u10D8\u10DC\u10EB\u10D8\u10E1": "\u10D0\u10E1\u10DE\u10D8\u10DC\u10EB\u10D0", "\u10D0\u10EE\u10D0\u10DA\u10E5\u10D0\u10DA\u10D0\u10E5\u10D8\u10E1": "\u10D0\u10EE\u10D0\u10DA\u10E5\u10D0\u10DA\u10D0\u10E5\u10D8", "\u10DC\u10D8\u10DC\u10DD\u10EC\u10DB\u10D8\u10DC\u10D3\u10D8\u10E1": "\u10DC\u10D8\u10DC\u10DD\u10EC\u10DB\u10D8\u10DC\u10D3\u10D0", "\u10EC\u10D0\u10DA\u10D9\u10D8\u10E1": "\u10EC\u10D0\u10DA\u10D9\u10D0", "\u10D3\u10DB\u10D0\u10DC\u10D8\u10E1\u10D8\u10E1": "\u10D3\u10DB\u10D0\u10DC\u10D8\u10E1\u10D8", "\u10D1\u10DD\u10DA\u10DC\u10D8\u10E1\u10D8\u10E1": "\u10D1\u10DD\u10DA\u10DC\u10D8\u10E1\u10D8", "\u10DB\u10D0\u10E0\u10DC\u10D4\u10E3\u10DA\u10D8\u10E1": "\u10DB\u10D0\u10E0\u10DC\u10D4\u10E3\u10DA\u10D8", "\u10D2\u10D0\u10E0\u10D3\u10D0\u10D1\u10DC\u10D8\u10E1": "\u10D2\u10D0\u10E0\u10D3\u10D0\u10D1\u10D0\u10DC\u10D8", "\u10D7\u10D4\u10D7\u10E0\u10D8\u10EC\u10E7\u10D0\u10E0\u10DD\u10E1": "\u10D7\u10D4\u10D7\u10E0\u10D8\u10EC\u10E7\u10D0\u10E0\u10DD", "\u10DD\u10DC\u10D8\u10E1\u10D0": "\u10DD\u10DC\u10D8", "\u10DD\u10DC\u10D8\u10E1": "\u10DD\u10DC\u10D8", "\u10D0\u10DB\u10D1\u10E0\u10DD\u10DA\u10D0\u10E3\u10E0\u10D8\u10E1": "\u10D0\u10DB\u10D1\u10E0\u10DD\u10DA\u10D0\u10E3\u10E0\u10D8", "\u10EA\u10D0\u10D2\u10D4\u10E0\u10D8\u10E1": "\u10EA\u10D0\u10D2\u10D4\u10E0\u10D8", "\u10DA\u10D4\u10DC\u10E2\u10D4\u10EE\u10D8\u10E1": "\u10DA\u10D4\u10DC\u10E2\u10D4\u10EE\u10D8", "\u10DB\u10D4\u10E1\u10E2\u10D8\u10D8\u10E1": "\u10DB\u10D4\u10E1\u10E2\u10D8\u10D0", "\u10E1\u10D0\u10E9\u10EE\u10D4\u10E0\u10D8\u10E1": "\u10E1\u10D0\u10E9\u10EE\u10D4\u10E0\u10D4", "\u10ED\u10D8\u10D0\u10D7\u10E3\u10E0\u10D8\u10E1": "\u10ED\u10D8\u10D0\u10D7\u10E3\u10E0\u10D0", "\u10EE\u10D0\u10E0\u10D0\u10D2\u10D0\u10E3\u10DA\u10D8\u10E1": "\u10EE\u10D0\u10E0\u10D0\u10D2\u10D0\u10E3\u10DA\u10D8", "\u10D6\u10D4\u10E1\u10E2\u10D0\u10E4\u10DD\u10DC\u10D8\u10E1": "\u10D6\u10D4\u10E1\u10E2\u10D0\u10E4\u10DD\u10DC\u10D8", "\u10D1\u10D0\u10E6\u10D3\u10D0\u10D7\u10D8\u10E1": "\u10D1\u10D0\u10E6\u10D3\u10D0\u10D7\u10D8", "\u10D5\u10D0\u10DC\u10D8\u10E1": "\u10D5\u10D0\u10DC\u10D8", "\u10E1\u10D0\u10DB\u10E2\u10E0\u10D4\u10D3\u10D8\u10D8\u10E1": "\u10E1\u10D0\u10DB\u10E2\u10E0\u10D4\u10D3\u10D8\u10D0", "\u10EE\u10DD\u10DC\u10D8\u10E1": "\u10EE\u10DD\u10DC\u10D8", "\u10EC\u10E7\u10D0\u10DA\u10E2\u10E3\u10D1\u10DD\u10E1": "\u10EC\u10E7\u10D0\u10DA\u10E2\u10E3\u10D1\u10DD", "\u10E2\u10E7\u10D8\u10D1\u10E3\u10DA\u10D8\u10E1": "\u10E2\u10E7\u10D8\u10D1\u10E3\u10DA\u10D8", "\u10D7\u10D4\u10E0\u10EF\u10DD\u10DA\u10D8\u10E1": "\u10D7\u10D4\u10E0\u10EF\u10DD\u10DA\u10D0", "\u10DD\u10D6\u10E3\u10E0\u10D2\u10D4\u10D7\u10D8\u10E1": "\u10DD\u10D6\u10E3\u10E0\u10D2\u10D4\u10D7\u10D8", "\u10DA\u10D0\u10DC\u10E9\u10EE\u10E3\u10D7\u10D8\u10E1": "\u10DA\u10D0\u10DC\u10E9\u10EE\u10E3\u10D7\u10D8", "\u10E9\u10DD\u10EE\u10D0\u10E2\u10D0\u10E3\u10E0\u10D8\u10E1": "\u10E9\u10DD\u10EE\u10D0\u10E2\u10D0\u10E3\u10E0\u10D8", "\u10D0\u10D1\u10D0\u10E8\u10D8\u10E1": "\u10D0\u10D1\u10D0\u10E8\u10D0", "\u10E1\u10D4\u10DC\u10D0\u10D9\u10D8\u10E1": "\u10E1\u10D4\u10DC\u10D0\u10D9\u10D8", "\u10DB\u10D0\u10E0\u10E2\u10D5\u10D8\u10DA\u10D8\u10E1": "\u10DB\u10D0\u10E0\u10E2\u10D5\u10D8\u10DA\u10D8", "\u10EE\u10DD\u10D1\u10D8\u10E1": "\u10EE\u10DD\u10D1\u10D8", "\u10D6\u10E3\u10D2\u10D3\u10D8\u10D3\u10D8\u10E1": "\u10D6\u10E3\u10D2\u10D3\u10D8\u10D3\u10D8", "\u10EC\u10D0\u10DA\u10D4\u10DC\u10EF\u10D8\u10EE\u10D8\u10E1": "\u10EC\u10D0\u10DA\u10D4\u10DC\u10EF\u10D8\u10EE\u10D0", "\u10E9\u10EE\u10DD\u10E0\u10DD\u10EC\u10E7\u10E3\u10E1": "\u10E9\u10EE\u10DD\u10E0\u10DD\u10EC\u10E7\u10E3", "\u10D1\u10D0\u10D7\u10E3\u10DB\u10D8\u10E1": "\u10D1\u10D0\u10D7\u10E3\u10DB\u10D8", "\u10E5\u10D4\u10D3\u10D8\u10E1": "\u10E5\u10D4\u10D3\u10D0", "\u10E5\u10DD\u10D1\u10E3\u10DA\u10D4\u10D7\u10D8\u10E1": "\u10E5\u10DD\u10D1\u10E3\u10DA\u10D4\u10D7\u10D8", "\u10E8\u10E3\u10D0\u10EE\u10D4\u10D5\u10D8\u10E1": "\u10E8\u10E3\u10D0\u10EE\u10D4\u10D5\u10D8", "\u10EE\u10D4\u10DA\u10D5\u10D0\u10E9\u10D0\u10E3\u10E0\u10D8\u10E1": "\u10EE\u10D4\u10DA\u10D5\u10D0\u10E9\u10D0\u10E3\u10E0\u10D8", "\u10EE\u10E3\u10DA\u10DD\u10E1": "\u10EE\u10E3\u10DA\u10DD", "\u10D2\u10E3\u10DA\u10E0\u10D8\u10E4\u10E8\u10D8\u10E1": "\u10D2\u10E3\u10DA\u10E0\u10D8\u10E4\u10E8\u10D8", "\u10D2\u10D0\u10DA\u10D8\u10E1": "\u10D2\u10D0\u10DA\u10D8", "\u10DD\u10E9\u10D0\u10DB\u10E9\u10D8\u10E0\u10D8\u10E1": "\u10DD\u10E9\u10D0\u10DB\u10E9\u10D8\u10E0\u10D4", "\u10E1\u10DD\u10EE\u10E3\u10DB\u10D8\u10E1": "\u10E1\u10DD\u10EE\u10E3\u10DB\u10D8", "\u10D2\u10E3\u10D3\u10D0\u10E3\u10D7\u10D8\u10E1": "\u10D2\u10E3\u10D3\u10D0\u10E3\u10D7\u10D0", "\u10D2\u10D0\u10D2\u10E0\u10D8\u10E1": "\u10D2\u10D0\u10D2\u10E0\u10D0", "\u10EA\u10EE\u10D8\u10DC\u10D5\u10D0\u10DA\u10D8\u10E1": "\u10EA\u10EE\u10D8\u10DC\u10D5\u10D0\u10DA\u10D8", "\u10EF\u10D0\u10D5\u10D8\u10E1": "\u10EF\u10D0\u10D5\u10D0", "\u10D0\u10EE\u10D0\u10DA\u10D2\u10DD\u10E0\u10D8\u10E1": "\u10D0\u10EE\u10D0\u10DA\u10D2\u10DD\u10E0\u10D8", "\u10D6\u10DC\u10D0\u10E3\u10E0\u10D8\u10E1": "\u10D6\u10DC\u10D0\u10E3\u10E0\u10D8" };
function normalizeMuniName(name) {
  if (!name) return "\u10E3\u10EA\u10DC\u10DD\u10D1\u10D8 \u10DB\u10E3\u10DC\u10D8\u10EA\u10D8\u10DE\u10D0\u10DA\u10D8\u10E2\u10D4\u10E2\u10D8";
  let n = name.replace(/ რაიონი$/, "").replace(/ მუნიციპალიტეტი$/, "");
  return muniNameMap[n] || n;
}
var app = (0, import_express.default)();
var PORT = 3e3;
app.use((0, import_compression.default)());
var geoCache = {
  meta: null,
  rawMuni: null,
  periods: {},
  trendFixed: null,
  trendMobile: null,
  ready: false
};
function normalizePoints(data) {
  return {
    ...data,
    features: data.features.map((f, idx) => ({
      ...f,
      properties: {
        ...f.properties,
        name: `\u10D6\u10DD\u10DC\u10D0 #${idx + 1}`,
        download: f.properties.avg_d_mbps || 0,
        upload: f.properties.avg_u_mbps || 0,
        ping: f.properties.avg_lat_ms || 0,
        tests: f.properties.tests || 0,
        devices: f.properties.devices || 0,
        locations: 1
      }
    }))
  };
}
async function aggregateData(pointsData, muniData) {
  const result = JSON.parse(JSON.stringify(muniData));
  const centroids = pointsData.features.map((f) => {
    const pt = turf.center(f);
    pt.properties = f.properties;
    return pt;
  });
  for (let i = 0; i < result.features.length; i++) {
    const muni = result.features[i];
    const name = normalizeMuniName(muni.properties.NAME_2 || muni.properties.NAME_1 || muni.properties.name);
    muni.properties.name = name;
    const ptsInPoly = [];
    if (muni.geometry && (muni.geometry.type === "Polygon" || muni.geometry.type === "MultiPolygon")) {
      const bbox2 = turf.bbox(muni);
      for (const pt of centroids) {
        try {
          const [lng, lat] = pt.geometry.coordinates;
          if (lng >= bbox2[0] && lng <= bbox2[2] && lat >= bbox2[1] && lat <= bbox2[3]) {
            if (turf.booleanPointInPolygon(pt, muni)) {
              ptsInPoly.push(pt.properties);
            }
          }
        } catch (err) {
        }
      }
    }
    let download_avg = 0, download_max = 0, download_min = 0;
    let upload_avg = 0, upload_max = 0, upload_min = 0;
    let ping_avg = 0, ping_max = 0, ping_min = 0;
    let tests = 0;
    let devices = 0;
    let locations = ptsInPoly.length;
    if (ptsInPoly.length > 0) {
      let dSum = 0, dCount = 0;
      let uSum = 0, uCount = 0;
      let pSum = 0, pCount = 0;
      for (const p of ptsInPoly) {
        if (p.download > 0) {
          dSum += p.download;
          dCount++;
          download_max = Math.max(download_max, p.download);
          download_min = download_min === 0 ? p.download : Math.min(download_min, p.download);
        }
        if (p.upload > 0) {
          uSum += p.upload;
          uCount++;
          upload_max = Math.max(upload_max, p.upload);
          upload_min = upload_min === 0 ? p.upload : Math.min(upload_min, p.upload);
        }
        if (p.ping > 0) {
          pSum += p.ping;
          pCount++;
          ping_max = Math.max(ping_max, p.ping);
          ping_min = ping_min === 0 ? p.ping : Math.min(ping_min, p.ping);
        }
        tests += p.tests || 0;
        devices += p.devices || 0;
      }
      if (dCount > 0) download_avg = dSum / dCount;
      if (uCount > 0) upload_avg = uSum / uCount;
      if (pCount > 0) ping_avg = pSum / pCount;
    }
    muni.properties.download = download_avg;
    muni.properties.download_max = download_max;
    muni.properties.download_min = download_min;
    muni.properties.upload = upload_avg;
    muni.properties.upload_max = upload_max;
    muni.properties.upload_min = upload_min;
    muni.properties.ping = ping_avg;
    muni.properties.ping_max = ping_max;
    muni.properties.ping_min = ping_min;
    muni.properties.tests = tests;
    muni.properties.devices = devices;
    muni.properties.locations = locations;
    if (i % 10 === 0) await new Promise((r) => setTimeout(r, 0));
  }
  return result;
}
function closeRings(geojson) {
  if (geojson.type === "FeatureCollection") {
    geojson.features.forEach((f) => closeRings(f));
  } else if (geojson.type === "Feature") {
    closeRings(geojson.geometry);
  } else if (geojson.type === "Polygon") {
    geojson.coordinates.forEach((ring) => {
      if (ring.length > 0) {
        const first = ring[0];
        const last = ring[ring.length - 1];
        if (first[0] !== last[0] || first[1] !== last[1]) {
          ring.push([...first]);
        }
      }
    });
  } else if (geojson.type === "MultiPolygon") {
    geojson.coordinates.forEach((poly) => {
      poly.forEach((ring) => {
        if (ring.length > 0) {
          const first = ring[0];
          const last = ring[ring.length - 1];
          if (first[0] !== last[0] || first[1] !== last[1]) {
            ring.push([...first]);
          }
        }
      });
    });
  }
  return geojson;
}
async function fetchTrendData(files, rawMuni) {
  const trend = {
    national: [],
    municipalities: {}
  };
  const baseUrl = "https://raw.githubusercontent.com/caucasusoffline/georgia-speedtest-map/main/data/";
  const muniBBoxes = rawMuni.features.map((m) => ({
    muni: m,
    name: normalizeMuniName(m.properties.NAME_2 || m.properties.NAME_1 || m.properties.name),
    bbox: turf.bbox(m)
  }));
  for (const mb of muniBBoxes) {
    trend.municipalities[mb.name] = [];
  }
  for (let i = 0; i < files.length; i += 3) {
    const chunk = files.slice(i, i + 3);
    const promises = chunk.map(async (file) => {
      try {
        const res = await fetch(baseUrl + file);
        const data = await res.json();
        let totalDown = 0, totalUp = 0, totalPing = 0;
        let count = 0;
        for (const f of data.features) {
          if (f.properties.avg_d_mbps > 0) {
            totalDown += f.properties.avg_d_mbps;
            totalUp += f.properties.avg_u_mbps;
            totalPing += f.properties.avg_lat_ms;
            count++;
          }
        }
        const match = file.match(/(\d{4})_(Q\d)/);
        const quarter = match ? `${match[1]} ${match[2]}` : file;
        const timestamp = match ? (/* @__PURE__ */ new Date(`${match[1]}-${match[2].replace("Q1", "01").replace("Q2", "04").replace("Q3", "07").replace("Q4", "10")}-01`)).getTime() : 0;
        const nationalData = {
          quarter,
          download: count > 0 ? totalDown / count : 0,
          upload: count > 0 ? totalUp / count : 0,
          ping: count > 0 ? totalPing / count : 0,
          timestamp
        };
        const muniStats = {};
        for (const mb of muniBBoxes) {
          muniStats[mb.name] = { mDown: 0, mUp: 0, mPing: 0, mCount: 0 };
        }
        const centroids = data.features.map((f) => {
          const pt = turf.center(f);
          pt.properties = f.properties;
          return pt;
        });
        let ptIdx = 0;
        for (const pt of centroids) {
          if (ptIdx++ % 1e3 === 0) await new Promise((r) => setTimeout(r, 0));
          if (pt.properties.avg_d_mbps <= 0) continue;
          const [lng, lat] = pt.geometry.coordinates;
          for (const mb of muniBBoxes) {
            if (lng >= mb.bbox[0] && lng <= mb.bbox[2] && lat >= mb.bbox[1] && lat <= mb.bbox[3]) {
              try {
                if (mb.muni.geometry && (mb.muni.geometry.type === "Polygon" || mb.muni.geometry.type === "MultiPolygon")) {
                  if (turf.booleanPointInPolygon(pt, mb.muni)) {
                    muniStats[mb.name].mDown += pt.properties.avg_d_mbps;
                    muniStats[mb.name].mUp += pt.properties.avg_u_mbps;
                    muniStats[mb.name].mPing += pt.properties.avg_lat_ms;
                    muniStats[mb.name].mCount++;
                    break;
                  }
                }
              } catch (e) {
              }
            }
          }
        }
        const finalMuniStats = {};
        for (const mb of muniBBoxes) {
          const s = muniStats[mb.name];
          finalMuniStats[mb.name] = {
            quarter,
            download: s.mCount > 0 ? s.mDown / s.mCount : 0,
            upload: s.mCount > 0 ? s.mUp / s.mCount : 0,
            ping: s.mCount > 0 ? s.mPing / s.mCount : 0,
            timestamp
          };
        }
        await new Promise((r) => setTimeout(r, 10));
        return { national: nationalData, municipalities: finalMuniStats };
      } catch (e) {
        return null;
      }
    });
    const results = await Promise.all(promises);
    for (const res of results) {
      if (res) {
        trend.national.push(res.national);
        for (const [name, stats] of Object.entries(res.municipalities)) {
          trend.municipalities[name].push(stats);
        }
      }
    }
  }
  trend.national.sort((a, b) => a.timestamp - b.timestamp);
  for (const name in trend.municipalities) {
    trend.municipalities[name].sort((a, b) => a.timestamp - b.timestamp);
  }
  return trend;
}
async function loadPeriodData(file) {
  if (geoCache.periods[file]) {
    geoCache.periods[file].lastAccessed = Date.now();
    return geoCache.periods[file];
  }
  const keys = Object.keys(geoCache.periods);
  if (keys.length >= 10) {
    let oldestKey = keys[0];
    let oldestTime = geoCache.periods[oldestKey].lastAccessed;
    for (const key of keys) {
      if (geoCache.periods[key].lastAccessed < oldestTime) {
        oldestTime = geoCache.periods[key].lastAccessed;
        oldestKey = key;
      }
    }
    delete geoCache.periods[oldestKey];
  }
  const baseUrl = "https://raw.githubusercontent.com/caucasusoffline/georgia-speedtest-map/main/data/";
  try {
    const res = await fetch(baseUrl + file);
    const raw = await res.json();
    const points = normalizePoints(raw);
    const agg = await aggregateData(points, geoCache.rawMuni);
    geoCache.periods[file] = { points, agg, lastAccessed: Date.now() };
    return geoCache.periods[file];
  } catch (e) {
    console.error("Error loading period data", file, e);
    return null;
  }
}
async function initData() {
  try {
    console.log("Fetching metadata...");
    const metaRes = await fetch("https://raw.githubusercontent.com/caucasusoffline/georgia-speedtest-map/main/data/metadata.json");
    const meta = await metaRes.json();
    geoCache.meta = meta;
    const latestFixed = meta.fixed[0];
    const latestMobile = meta.mobile[0];
    console.log("Fetching muni shapes...");
    const muniRes = await fetch("https://caucasusoffline.com/test1000/js/municipality-shapes-converted.geojson");
    let rawMuni = await muniRes.json();
    rawMuni = closeRings(rawMuni);
    geoCache.rawMuni = rawMuni;
    console.log("Loading latest datasets...");
    await loadPeriodData(latestFixed);
    await loadPeriodData(latestMobile);
    geoCache.ready = true;
    console.log("Map data init complete.");
    console.log("Fetching trend data...");
    geoCache.trendFixed = await fetchTrendData(meta.fixed, rawMuni);
    geoCache.trendMobile = await fetchTrendData(meta.mobile, rawMuni);
    console.log("Trend data init complete.");
  } catch (e) {
    console.error("Failed to init data", e);
  }
}
initData();
async function startServer() {
  app.get("/api/metadata", (req, res) => {
    if (!geoCache.ready) return res.status(503).json({ error: "Data is loading" });
    res.setHeader("Cache-Control", "public, max-age=3600");
    res.json(geoCache.meta);
  });
  app.get("/api/data", async (req, res) => {
    if (!geoCache.ready) {
      return res.status(503).json({ error: "Data is still processing on the server. Please try again in a few seconds." });
    }
    const type = req.query.type || "fixed";
    const view = req.query.view || "municipality";
    const period = req.query.period;
    const file = period ? period : geoCache.meta[type][0];
    let periodData = geoCache.periods[file];
    if (!periodData) {
      periodData = await loadPeriodData(file);
    }
    if (!periodData) {
      return res.status(404).json({ error: "Data not found" });
    }
    res.setHeader("Cache-Control", "public, max-age=86400");
    if (view === "points") {
      res.json(periodData.points);
    } else {
      res.json(periodData.agg);
    }
  });
  app.get("/api/trend", (req, res) => {
    const type = req.query.type || "fixed";
    const data = type === "mobile" ? geoCache.trendMobile : geoCache.trendFixed;
    if (!data) {
      return res.status(503).json({ error: "Trend data is still processing" });
    }
    res.setHeader("Cache-Control", "public, max-age=3600");
    res.json(data);
  });
  if (process.env.NODE_ENV !== "production") {
    const vite = await (0, import_vite.createServer)({
      server: { middlewareMode: true },
      appType: "spa"
    });
    app.use(vite.middlewares);
  } else {
    const distPath = import_path.default.join(process.cwd(), "dist");
    app.use(import_express.default.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(import_path.default.join(distPath, "index.html"));
    });
  }
  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}
startServer();
//# sourceMappingURL=server.cjs.map
