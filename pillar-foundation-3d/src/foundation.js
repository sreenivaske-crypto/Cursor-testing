import * as THREE from 'three'
import { CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js'

/** Typical isolated-footing frame for a 5-storey RCC building (metres). */
export const SPECS = {
  colsX: 4,
  colsZ: 3,
  bay: 5.0,
  column: 0.45,
  footing: 2.0,
  footingDepth: 0.5,
  foundingDepth: 1.8,
  pedestalExtra: 0.05,
  plinthBeamW: 0.3,
  plinthBeamH: 0.45,
  floorBeamW: 0.3,
  floorBeamH: 0.45,
  storeyHeight: 3.2,
  stories: 5,
  slabThickness: 0.15,
}

export function createFoundationModel() {
  const root = new THREE.Group()
  root.name = 'foundationRoot'

  const layers = {
    soil: new THREE.Group(),
    footings: new THREE.Group(),
    beams: new THREE.Group(),
    columns: new THREE.Group(),
    slabs: new THREE.Group(),
    envelope: new THREE.Group(),
    labels: new THREE.Group(),
  }

  Object.entries(layers).forEach(([name, group]) => {
    group.name = name
    root.add(group)
  })

  const materials = createMaterials()
  const positions = columnGrid()

  buildSoil(layers.soil, materials)
  buildFootings(layers.footings, materials, positions)
  buildColumns(layers.columns, materials, positions)
  buildBeams(layers.beams, materials, positions)
  buildSlabs(layers.slabs, materials)
  buildEnvelope(layers.envelope, materials)
  buildLabels(layers.labels, positions)

  return { root, layers, materials, specs: SPECS }
}

function createMaterials() {
  return {
    footing: new THREE.MeshStandardMaterial({
      color: 0xc4b7a2,
      roughness: 0.92,
      metalness: 0.02,
    }),
    column: new THREE.MeshStandardMaterial({
      color: 0x8f9a8a,
      roughness: 0.85,
      metalness: 0.04,
    }),
    beam: new THREE.MeshStandardMaterial({
      color: 0x6e7d6e,
      roughness: 0.82,
      metalness: 0.04,
    }),
    slab: new THREE.MeshStandardMaterial({
      color: 0xb8c0b4,
      roughness: 0.9,
      metalness: 0.02,
      transparent: true,
      opacity: 0.55,
    }),
    soil: new THREE.MeshStandardMaterial({
      color: 0x8a6a45,
      roughness: 1,
      metalness: 0,
    }),
    soilDark: new THREE.MeshStandardMaterial({
      color: 0x6b5134,
      roughness: 1,
      metalness: 0,
    }),
    grass: new THREE.MeshStandardMaterial({
      color: 0x6f8f62,
      roughness: 1,
      metalness: 0,
    }),
    envelope: new THREE.MeshStandardMaterial({
      color: 0xdfe8dc,
      roughness: 0.2,
      metalness: 0.05,
      transparent: true,
      opacity: 0.12,
      side: THREE.DoubleSide,
      depthWrite: false,
    }),
    edge: new THREE.LineBasicMaterial({ color: 0x3d4a3d, transparent: true, opacity: 0.35 }),
  }
}

function columnGrid() {
  const { colsX, colsZ, bay } = SPECS
  const originX = -((colsX - 1) * bay) / 2
  const originZ = -((colsZ - 1) * bay) / 2
  const positions = []

  for (let ix = 0; ix < colsX; ix += 1) {
    for (let iz = 0; iz < colsZ; iz += 1) {
      positions.push({
        x: originX + ix * bay,
        z: originZ + iz * bay,
        ix,
        iz,
      })
    }
  }

  return positions
}

function addEdges(mesh, material) {
  const edges = new THREE.EdgesGeometry(mesh.geometry, 20)
  const lines = new THREE.LineSegments(edges, material)
  lines.position.copy(mesh.position)
  lines.rotation.copy(mesh.rotation)
  lines.scale.copy(mesh.scale)
  mesh.parent.add(lines)
  return lines
}

function buildSoil(group, materials) {
  const { colsX, colsZ, bay, foundingDepth, footing } = SPECS
  const width = (colsX - 1) * bay + footing * 2.8
  const depth = (colsZ - 1) * bay + footing * 2.8
  const pitMargin = footing * 0.9
  const pitW = (colsX - 1) * bay + pitMargin * 2
  const pitD = (colsZ - 1) * bay + pitMargin * 2

  // Surrounding ground (top surface with a rectangular opening via separate pads)
  const groundY = 0
  const surround = new THREE.Group()
  surround.name = 'groundSurround'

  const pads = [
    { x: 0, z: -(pitD + (depth - pitD) / 2) / 2, w: width, d: (depth - pitD) / 2 },
    { x: 0, z: (pitD + (depth - pitD) / 2) / 2, w: width, d: (depth - pitD) / 2 },
    { x: -(pitW + (width - pitW) / 2) / 2, z: 0, w: (width - pitW) / 2, d: pitD },
    { x: (pitW + (width - pitW) / 2) / 2, z: 0, w: (width - pitW) / 2, d: pitD },
  ]

  pads.forEach((p) => {
    if (p.w <= 0.01 || p.d <= 0.01) return
    const grass = new THREE.Mesh(
      new THREE.BoxGeometry(p.w, 0.08, p.d),
      materials.grass,
    )
    grass.position.set(p.x, groundY + 0.04, p.z)
    grass.receiveShadow = true
    surround.add(grass)

    const soilBlock = new THREE.Mesh(
      new THREE.BoxGeometry(p.w, foundingDepth, p.d),
      materials.soil,
    )
    soilBlock.position.set(p.x, -foundingDepth / 2, p.z)
    soilBlock.receiveShadow = true
    surround.add(soilBlock)
  })

  group.add(surround)

  // Excavation pit walls
  const wallT = 0.35
  const wallH = foundingDepth
  const walls = [
    { x: 0, z: -pitD / 2 - wallT / 2, w: pitW + wallT * 2, d: wallT },
    { x: 0, z: pitD / 2 + wallT / 2, w: pitW + wallT * 2, d: wallT },
    { x: -pitW / 2 - wallT / 2, z: 0, w: wallT, d: pitD },
    { x: pitW / 2 + wallT / 2, z: 0, w: wallT, d: pitD },
  ]

  walls.forEach((w) => {
    const mesh = new THREE.Mesh(
      new THREE.BoxGeometry(w.w, wallH, w.d),
      materials.soilDark,
    )
    mesh.position.set(w.x, -wallH / 2, w.z)
    mesh.receiveShadow = true
    group.add(mesh)
  })

  // Pit floor bedding
  const bedding = new THREE.Mesh(
    new THREE.BoxGeometry(pitW, 0.12, pitD),
    materials.soilDark,
  )
  bedding.position.set(0, -foundingDepth + 0.06, 0)
  bedding.receiveShadow = true
  group.add(bedding)

  // Ground level marker plane (thin translucent cut)
  const glPlane = new THREE.Mesh(
    new THREE.PlaneGeometry(width * 1.05, depth * 1.05),
    new THREE.MeshBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.05,
      side: THREE.DoubleSide,
      depthWrite: false,
    }),
  )
  glPlane.rotation.x = -Math.PI / 2
  glPlane.position.y = 0.002
  group.add(glPlane)
}

function buildFootings(group, materials, positions) {
  const { footing, footingDepth, foundingDepth, column, pedestalExtra } = SPECS
  const footingTop = -foundingDepth + footingDepth
  const plinthTop = 0.45

  positions.forEach(({ x, z }) => {
    const pad = new THREE.Mesh(
      new THREE.BoxGeometry(footing, footingDepth, footing),
      materials.footing,
    )
    pad.position.set(x, -foundingDepth + footingDepth / 2, z)
    pad.castShadow = true
    pad.receiveShadow = true
    group.add(pad)
    addEdges(pad, materials.edge)

    // Pedestal from footing top up to plinth beam soffit
    const pedSize = column + pedestalExtra
    const pedH = plinthTop - footingTop
    const pedestal = new THREE.Mesh(
      new THREE.BoxGeometry(pedSize, pedH, pedSize),
      materials.footing,
    )
    pedestal.position.set(x, footingTop + pedH / 2, z)
    pedestal.castShadow = true
    pedestal.receiveShadow = true
    group.add(pedestal)
    addEdges(pedestal, materials.edge)
  })
}

function buildColumns(group, materials, positions) {
  const { column, storeyHeight, stories } = SPECS
  const totalH = stories * storeyHeight
  const baseY = 0.45

  positions.forEach(({ x, z }) => {
    const col = new THREE.Mesh(
      new THREE.BoxGeometry(column, totalH, column),
      materials.column,
    )
    col.position.set(x, baseY + totalH / 2, z)
    col.castShadow = true
    col.receiveShadow = true
    group.add(col)
    addEdges(col, materials.edge)
  })
}

function buildBeams(group, materials, positions) {
  const {
    colsX,
    colsZ,
    bay,
    column,
    plinthBeamW,
    plinthBeamH,
    floorBeamW,
    floorBeamH,
    storeyHeight,
    stories,
  } = SPECS

  const byRow = Array.from({ length: colsZ }, () => [])
  const byCol = Array.from({ length: colsX }, () => [])

  positions.forEach((p) => {
    byRow[p.iz].push(p)
    byCol[p.ix].push(p)
  })

  const makeBeam = (length, w, h, x, y, z, rotY = 0) => {
    const mesh = new THREE.Mesh(
      new THREE.BoxGeometry(length, h, w),
      materials.beam,
    )
    mesh.position.set(x, y, z)
    mesh.rotation.y = rotY
    mesh.castShadow = true
    mesh.receiveShadow = true
    group.add(mesh)
    addEdges(mesh, materials.edge)
  }

  const span = bay - column
  const levels = [0.45] // plinth
  for (let s = 1; s <= stories; s += 1) {
    levels.push(0.45 + s * storeyHeight)
  }

  levels.forEach((levelY, idx) => {
    const w = idx === 0 ? plinthBeamW : floorBeamW
    const h = idx === 0 ? plinthBeamH : floorBeamH
    const y = levelY - h / 2

    // Beams along X (between columns in a row)
    byRow.forEach((row) => {
      row.sort((a, b) => a.x - b.x)
      for (let i = 0; i < row.length - 1; i += 1) {
        const a = row[i]
        const b = row[i + 1]
        const midX = (a.x + b.x) / 2
        makeBeam(span, w, h, midX, y, a.z, 0)
      }
    })

    // Beams along Z (between columns in a column line)
    byCol.forEach((col) => {
      col.sort((a, b) => a.z - b.z)
      for (let i = 0; i < col.length - 1; i += 1) {
        const a = col[i]
        const b = col[i + 1]
        const midZ = (a.z + b.z) / 2
        makeBeam(span, w, h, a.x, y, midZ, Math.PI / 2)
      }
    })
  })
}

function buildSlabs(group, materials) {
  const {
    colsX,
    colsZ,
    bay,
    column,
    storeyHeight,
    stories,
    slabThickness,
    floorBeamH,
  } = SPECS

  const slabW = (colsX - 1) * bay + column
  const slabD = (colsZ - 1) * bay + column

  for (let s = 1; s <= stories; s += 1) {
    const levelY = 0.45 + s * storeyHeight
    const slab = new THREE.Mesh(
      new THREE.BoxGeometry(slabW, slabThickness, slabD),
      materials.slab,
    )
    slab.position.set(0, levelY - floorBeamH + slabThickness / 2, 0)
    slab.receiveShadow = true
    group.add(slab)
  }
}

function buildEnvelope(group, materials) {
  const { colsX, colsZ, bay, column, storeyHeight, stories } = SPECS
  const w = (colsX - 1) * bay + column + 0.4
  const d = (colsZ - 1) * bay + column + 0.4
  const h = stories * storeyHeight + 0.6
  const envelope = new THREE.Mesh(
    new THREE.BoxGeometry(w, h, d),
    materials.envelope,
  )
  envelope.position.set(0, 0.45 + h / 2, 0)
  group.add(envelope)

  const edges = new THREE.LineSegments(
    new THREE.EdgesGeometry(envelope.geometry),
    new THREE.LineBasicMaterial({ color: 0x5a6b5a, transparent: true, opacity: 0.45 }),
  )
  edges.position.copy(envelope.position)
  group.add(edges)
}

function makeLabel(text, position) {
  const el = document.createElement('div')
  el.className = 'dim-label'
  el.textContent = text
  Object.assign(el.style, {
    padding: '4px 8px',
    borderRadius: '8px',
    background: 'rgba(248,246,240,0.92)',
    border: '1px solid rgba(28,36,28,0.12)',
    color: '#1c241c',
    fontFamily: '"DM Sans", sans-serif',
    fontSize: '11px',
    fontWeight: '600',
    whiteSpace: 'nowrap',
    pointerEvents: 'none',
    boxShadow: '0 8px 20px rgba(20,28,20,0.12)',
  })
  const obj = new CSS2DObject(el)
  obj.position.copy(position)
  return obj
}

function buildLabels(group, positions) {
  const { footing, footingDepth, foundingDepth, column, bay, storeyHeight, stories } = SPECS
  const corner = positions.find((p) => p.ix === 0 && p.iz === 0)
  if (!corner) return

  group.add(
    makeLabel(
      `Pad footing ${footing.toFixed(1)}×${footing.toFixed(1)}×${footingDepth.toFixed(2)} m`,
      new THREE.Vector3(corner.x - footing * 0.7, -foundingDepth + footingDepth + 0.35, corner.z - footing * 0.7),
    ),
  )
  group.add(
    makeLabel(
      `Founding depth ${foundingDepth.toFixed(1)} m`,
      new THREE.Vector3(corner.x - bay * 0.55, -foundingDepth / 2, corner.z),
    ),
  )
  group.add(
    makeLabel(
      `Column ${Math.round(column * 1000)}×${Math.round(column * 1000)} mm`,
      new THREE.Vector3(corner.x, 2.2, corner.z - 0.9),
    ),
  )
  group.add(
    makeLabel(
      `Bay ${bay.toFixed(1)} m c/c`,
      new THREE.Vector3(corner.x + bay / 2, 0.9, corner.z - 1.4),
    ),
  )
  group.add(
    makeLabel(
      `5 storeys × ${storeyHeight.toFixed(1)} m`,
      new THREE.Vector3(0, 0.45 + stories * storeyHeight + 1.2, 0),
    ),
  )
  group.add(
    makeLabel('Ground level (GL)', new THREE.Vector3(bay * 1.6, 0.35, -bay)),
  )
}
