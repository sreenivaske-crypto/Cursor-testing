import './style.css'
import * as THREE from 'three'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
import { CSS2DRenderer } from 'three/addons/renderers/CSS2DRenderer.js'
import { createFoundationModel } from './foundation.js'

const canvas = document.querySelector('#scene')
const renderer = new THREE.WebGLRenderer({
  canvas,
  antialias: true,
  alpha: true,
})
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
renderer.setSize(window.innerWidth, window.innerHeight)
renderer.shadowMap.enabled = true
renderer.shadowMap.type = THREE.PCFShadowMap
renderer.outputColorSpace = THREE.SRGBColorSpace
renderer.toneMapping = THREE.ACESFilmicToneMapping
renderer.toneMappingExposure = 1.05

const labelRenderer = new CSS2DRenderer()
labelRenderer.setSize(window.innerWidth, window.innerHeight)
labelRenderer.domElement.style.position = 'absolute'
labelRenderer.domElement.style.inset = '0'
labelRenderer.domElement.style.pointerEvents = 'none'
document.querySelector('#app').appendChild(labelRenderer.domElement)

const scene = new THREE.Scene()
scene.background = new THREE.Color(0xd7e0d4)
scene.fog = new THREE.Fog(0xd7e0d4, 40, 90)

const camera = new THREE.PerspectiveCamera(
  42,
  window.innerWidth / window.innerHeight,
  0.1,
  200,
)

const controls = new OrbitControls(camera, renderer.domElement)
controls.enableDamping = true
controls.dampingFactor = 0.06
controls.minDistance = 8
controls.maxDistance = 70
controls.maxPolarAngle = Math.PI * 0.49
controls.target.set(0, 4, 0)

const hemi = new THREE.HemisphereLight(0xf4f7ef, 0x6b5a42, 1.1)
scene.add(hemi)

const sun = new THREE.DirectionalLight(0xfff3df, 1.35)
sun.position.set(18, 28, 12)
sun.castShadow = true
sun.shadow.mapSize.set(2048, 2048)
sun.shadow.camera.near = 1
sun.shadow.camera.far = 80
sun.shadow.camera.left = -30
sun.shadow.camera.right = 30
sun.shadow.camera.top = 30
sun.shadow.camera.bottom = -30
sun.shadow.bias = -0.0002
scene.add(sun)

const fill = new THREE.DirectionalLight(0xc9d7ff, 0.35)
fill.position.set(-16, 10, -10)
scene.add(fill)

const { root, layers } = createFoundationModel()
scene.add(root)

const home = {
  position: new THREE.Vector3(22, 16, 24),
  target: new THREE.Vector3(0, 4, 0),
}

function resetCamera() {
  camera.position.copy(home.position)
  controls.target.copy(home.target)
  controls.update()
}

resetCamera()

let exploded = false
const basePositions = new Map()

function captureBasePositions() {
  Object.values(layers).forEach((layer) => {
    layer.traverse((obj) => {
      if (obj.isMesh || obj.isLineSegments || obj.isCSS2DObject) {
        basePositions.set(obj.uuid, obj.position.clone())
      }
    })
  })
}

captureBasePositions()

function setExploded(on) {
  exploded = on
  const offsets = {
    soil: new THREE.Vector3(0, on ? -1.2 : 0, 0),
    footings: new THREE.Vector3(0, on ? -0.4 : 0, 0),
    beams: new THREE.Vector3(0, on ? 0.6 : 0, 0),
    columns: new THREE.Vector3(0, on ? 1.4 : 0, 0),
    slabs: new THREE.Vector3(0, on ? 2.2 : 0, 0),
    envelope: new THREE.Vector3(0, on ? 3.2 : 0, 0),
    labels: new THREE.Vector3(0, on ? 0.8 : 0, 0),
  }

  Object.entries(layers).forEach(([name, layer]) => {
    const offset = offsets[name] || new THREE.Vector3()
    layer.position.copy(offset)
  })

  document.querySelector('#btn-explode').textContent = on
    ? 'Compact view'
    : 'Exploded view'
}

document.querySelector('#toggles').addEventListener('change', (event) => {
  const input = event.target
  if (!(input instanceof HTMLInputElement)) return
  const layerName = input.dataset.layer
  if (!layerName || !layers[layerName]) return
  layers[layerName].visible = input.checked
})

document.querySelector('#btn-reset').addEventListener('click', resetCamera)
document.querySelector('#btn-explode').addEventListener('click', () => {
  setExploded(!exploded)
})

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight
  camera.updateProjectionMatrix()
  renderer.setSize(window.innerWidth, window.innerHeight)
  labelRenderer.setSize(window.innerWidth, window.innerHeight)
})

function animate() {
  requestAnimationFrame(animate)
  controls.update()
  renderer.render(scene, camera)
  labelRenderer.render(scene, camera)
}

animate()
