let map = null;
let vehicleMarker = null;
let selectedImage = null;


document.addEventListener("DOMContentLoaded", function () {

    console.log("FOGSAFE Dashboard loaded");

    initializeMap();

    initializeImageAnalysis();

    updateClock();

    getVehicleState();

    setInterval(getVehicleState, 1000);

    setInterval(updateClock, 1000);

});


/* =====================================================
   MAP
   ===================================================== */

function initializeMap() {

    const mapElement = document.getElementById("map");

    if (!mapElement) {
        console.warn("Map element not found");
        return;
    }

    if (typeof L === "undefined") {
        console.error("Leaflet is not loaded");
        return;
    }

    map = L.map("map").setView(
        [19.0760, 72.8777],
        16
    );

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            maxZoom: 20,
            attribution: "&copy; OpenStreetMap contributors"
        }
    ).addTo(map);

    vehicleMarker = L.marker(
        [19.0760, 72.8777]
    )
    .addTo(map)
    .bindPopup("FOGSAFE Vehicle");

}


/* =====================================================
   VEHICLE API
   ===================================================== */

async function getVehicleState() {

    try {

        const response = await fetch("/api/vehicle");

        if (!response.ok) {
            throw new Error(
                "Vehicle API returned " +
                response.status
            );
        }

        const data = await response.json();

        updateSpeed(
            data.speed,
            data.recommended_speed
        );

        updateObjectInfo(data);

        updateSafety(
            data.safety,
            data.object,
            data.distance
        );

        updateTelemetry(data);

        updateMap(
            data.latitude,
            data.longitude
        );

    } catch (error) {

        console.error(
            "Vehicle API error:",
            error
        );

    }

}


/* =====================================================
   SPEED
   ===================================================== */

function updateSpeed(
    speed,
    recommendedSpeed
) {

    const speedValue =
        document.getElementById("speedValue");

    const recommended =
        document.getElementById("recommendedSpeed");

    const needle =
        document.getElementById("speedNeedle");


    const currentSpeed =
        Number(speed || 0);

    const safeSpeed =
        Number(recommendedSpeed || 0);


    if (speedValue) {

        speedValue.textContent =
            currentSpeed.toFixed(1);

    }


    if (recommended) {

        recommended.textContent =
            safeSpeed.toFixed(1);

    }


    if (needle) {

        const maxSpeed = 60;

        const percentage =
            Math.min(
                Math.max(
                    currentSpeed / maxSpeed,
                    0
                ),
                1
            );

        const angle =
            -120 +
            percentage * 240;

        needle.style.transform =
            "rotate(" + angle + "deg)";

    }

}


/* =====================================================
   DETECTED OBJECT
   ===================================================== */

function updateObjectInfo(data) {

    const objectName =
        document.getElementById("objectName");

    const objectDistance =
        document.getElementById("objectDistance");

    const objectDirection =
        document.getElementById("objectDirection");


    const object =
        data.object || "NONE";

    const distance =
        Number(data.distance || 0);

    const direction =
        data.direction || "CLEAR";


    if (objectName) {

        objectName.textContent =
            object;

    }


    if (objectDistance) {

        if (distance > 0) {

            objectDistance.textContent =
                distance.toFixed(1) + " m";

        } else {

            objectDistance.textContent =
                "--";

        }

    }


    if (objectDirection) {

        objectDirection.textContent =
            direction;

    }

}


/* =====================================================
   SAFETY
   ===================================================== */

function updateSafety(
    safety,
    objectName,
    distance
) {

    const panel =
        document.getElementById(
            "safetyPanel"
        );

    const icon =
        document.getElementById(
            "safetyIcon"
        );

    const action =
        document.getElementById(
            "safetyAction"
        );

    const reason =
        document.getElementById(
            "safetyReason"
        );

    const bottomSafety =
        document.getElementById(
            "bottomSafety"
        );


    if (!panel) {
        return;
    }


    const object =
        objectName || "NONE";

    const dist =
        Number(distance || 0);


    if (safety === "STOP") {

        panel.className =
            "safety-panel danger";

        if (icon) {
            icon.textContent = "!";
        }

        if (action) {
            action.textContent = "STOP";
        }

        if (reason) {

            reason.textContent =
                object +
                " TOO CLOSE - " +
                dist.toFixed(1) +
                " m";

        }

        if (bottomSafety) {

            bottomSafety.textContent =
                "SAFETY: STOP";

        }

    }

    else if (safety === "CAUTION") {

        panel.className =
            "safety-panel caution";

        if (icon) {
            icon.textContent = "!";
        }

        if (action) {
            action.textContent =
                "SLOW DOWN";
        }

        if (reason) {

            reason.textContent =
                object +
                " AT " +
                dist.toFixed(1) +
                " m";

        }

        if (bottomSafety) {

            bottomSafety.textContent =
                "SAFETY: CAUTION";

        }

    }

    else {

        panel.className =
            "safety-panel safe";

        if (icon) {
            icon.textContent = "✓";
        }

        if (action) {
            action.textContent =
                "CONTINUE";
        }

        if (reason) {

            if (object === "NONE") {

                reason.textContent =
                    "PATH CLEAR";

            } else {

                reason.textContent =
                    object +
                    " DETECTED AT " +
                    dist.toFixed(1) +
                    " m";

            }

        }

        if (bottomSafety) {

            bottomSafety.textContent =
                "SAFETY: SAFE";

        }

    }

}


/* =====================================================
   TELEMETRY
   ===================================================== */

function updateTelemetry(data) {

    const visibilityValue =
        document.getElementById(
            "visibilityValue"
        );

    const latitude =
        document.getElementById(
            "latitude"
        );

    const longitude =
        document.getElementById(
            "longitude"
        );

    const altitude =
        document.getElementById(
            "altitude"
        );

    const heading =
        document.getElementById(
            "heading"
        );


    const visibility =
        Number(data.visibility || 0);

    const lat =
        Number(data.latitude || 0);

    const lng =
        Number(data.longitude || 0);

    const alt =
        Number(data.altitude || 0);

    const head =
        Number(data.heading || 0);


    if (visibilityValue) {

        visibilityValue.textContent =
            visibility.toFixed(1) + " m";

    }


    if (latitude) {

        latitude.textContent =
            lat.toFixed(6);

    }


    if (longitude) {

        longitude.textContent =
            lng.toFixed(6);

    }


    if (altitude) {

        altitude.textContent =
            alt.toFixed(1) + " m";

    }


    if (heading) {

        heading.textContent =
            head.toFixed(0) + "°";

    }


    const fogLevel =
        document.getElementById(
            "fogLevel"
        );


    if (fogLevel) {

        if (visibility < 4) {

            fogLevel.textContent =
                "DENSE FOG";

        }

        else if (visibility < 7) {

            fogLevel.textContent =
                "MODERATE FOG";

        }

        else {

            fogLevel.textContent =
                "CLEAR";

        }

    }


    const visibilityFill =
        document.getElementById(
            "visibilityFill"
        );


    if (visibilityFill) {

        const percentage =
            Math.min(
                Math.max(
                    (visibility / 10) * 100,
                    0
                ),
                100
            );

        visibilityFill.style.width =
            percentage + "%";

    }

}


/* =====================================================
   MAP UPDATE
   ===================================================== */

function updateMap(
    latitude,
    longitude
) {

    if (!map || !vehicleMarker) {
        return;
    }


    const lat =
        Number(latitude);

    const lng =
        Number(longitude);


    if (
        !Number.isFinite(lat) ||
        !Number.isFinite(lng) ||
        lat === 0 ||
        lng === 0
    ) {

        return;

    }


    vehicleMarker.setLatLng(
        [lat, lng]
    );

    map.panTo(
        [lat, lng]
    );

}


/* =====================================================
   CLOCK
   ===================================================== */

function updateClock() {

    const clock =
        document.getElementById(
            "currentTime"
        );

    if (!clock) {
        return;
    }


    const now =
        new Date();


    const hours =
        String(
            now.getHours()
        ).padStart(2, "0");


    const minutes =
        String(
            now.getMinutes()
        ).padStart(2, "0");


    const seconds =
        String(
            now.getSeconds()
        ).padStart(2, "0");


    clock.textContent =
        hours +
        ":" +
        minutes +
        ":" +
        seconds;

}


/* =====================================================
   IMAGE ANALYSIS
   ===================================================== */

function initializeImageAnalysis() {

    const imageInput =
        document.getElementById(
            "imageInput"
        );

    const analyzeButton =
        document.getElementById(
            "analyzeImageButton"
        );

    const clearButton =
        document.getElementById(
            "clearImageButton"
        );

    const analyzedImage =
        document.getElementById(
            "analyzedImage"
        );

    const placeholder =
        document.getElementById(
            "uploadPlaceholder"
        );

    const status =
        document.getElementById(
            "analysisStatus"
        );


    const modal =
        document.getElementById(
            "imageAnalysisModal"
        );

    const openModalBtn =
        document.getElementById(
            "openImageAnalysis"
        );

    const closeModalBtn =
        document.getElementById(
            "closeAnalysisButton"
        );


    /* OPEN MODAL */

    if (openModalBtn && modal) {

        openModalBtn.addEventListener(
            "click",
            function () {

                modal.classList.add(
                    "active"
                );

            }
        );

    }


    /* CLOSE MODAL */

    if (closeModalBtn && modal) {

        closeModalBtn.addEventListener(
            "click",
            function () {

                modal.classList.remove(
                    "active"
                );

            }
        );

    }


    if (!imageInput) {

        console.warn(
            "imageInput not found"
        );

        return;

    }


    console.log(
        "Image analysis initialized"
    );


    /* IMAGE SELECTED */

    imageInput.addEventListener(
        "change",
        function () {

            const file =
                imageInput.files[0];


            if (!file) {
                return;
            }


            if (
                !file.type.startsWith(
                    "image/"
                )
            ) {

                if (status) {

                    status.textContent =
                        "INVALID IMAGE";

                }

                return;

            }


            selectedImage =
                file;


            if (status) {

                status.textContent =
                    "IMAGE SELECTED";

            }


            if (analyzeButton) {

                analyzeButton.disabled =
                    false;

            }


            if (clearButton) {

                clearButton.disabled =
                    false;

            }


            const reader =
                new FileReader();


            reader.onload =
                function (event) {

                    if (analyzedImage) {

                        analyzedImage.src =
                            event.target.result;

                        analyzedImage.style.display =
                            "block";

                    }


                    if (placeholder) {

                        placeholder.style.display =
                            "none";

                    }

                };


            reader.readAsDataURL(
                file
            );

        }
    );


    /* ANALYZE BUTTON */

    if (analyzeButton) {

        analyzeButton.addEventListener(
            "click",
            analyzeSelectedImage
        );

    }


    /* CLEAR BUTTON */

    if (clearButton) {

        clearButton.addEventListener(
            "click",
            clearSelectedImage
        );

    }

}


/* =====================================================
   ANALYZE SELECTED IMAGE
   ===================================================== */

async function analyzeSelectedImage() {

    if (!selectedImage) {

        console.warn(
            "No image selected"
        );

        return;

    }


    const status =
        document.getElementById(
            "analysisStatus"
        );

    const analyzeButton =
        document.getElementById(
            "analyzeImageButton"
        );

    const detectionCount =
        document.getElementById(
            "imageDetectionCount"
        );

    const detectionList =
        document.getElementById(
            "imageDetectionList"
        );

    const analyzedImage =
        document.getElementById(
            "analyzedImage"
        );


    if (status) {

        status.textContent =
            "ANALYZING...";

    }


    if (analyzeButton) {

        analyzeButton.disabled =
            true;

    }


    const formData =
        new FormData();


    formData.append(
        "image",
        selectedImage
    );


    try {

        console.log(
            "Uploading image..."
        );


        const response =
            await fetch(
                "/api/analyze-image",
                {
                    method: "POST",
                    body: formData
                }
            );


        console.log(
            "Response status:",
            response.status
        );


        const data =
            await response.json();


        console.log(
            "Analysis result:",
            data
        );


        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.error ||
                "Image analysis failed"
            );

        }


        if (
            data.image &&
            analyzedImage
        ) {

            analyzedImage.src =
                data.image;

            analyzedImage.style.display =
                "block";

        }


        if (detectionCount) {

            detectionCount.textContent =
                "Objects Detected: " +
                (data.count || 0);

        }


        if (detectionList) {

            detectionList.innerHTML =
                "";


            if (
                !data.detections ||
                data.detections.length === 0
            ) {

                detectionList.textContent =
                    "No trained objects detected.";

            }

            else {

                data.detections.forEach(
                    function (detection) {

                        const item =
                            document.createElement(
                                "div"
                            );


                        item.className =
                            "image-detection-item";


                        item.textContent =
                            (detection.object ||
                                "OBJECT") +
                            " - " +
                            (detection.confidence ||
                                0) +
                            "%";


                        detectionList.appendChild(
                            item
                        );

                    }
                );

            }

        }


        if (status) {

            status.textContent =
                "ANALYSIS COMPLETE";

        }


    }

    catch (error) {

        console.error(
            "Image analysis error:",
            error
        );


        if (status) {

            status.textContent =
                "ANALYSIS FAILED";

        }


        if (detectionList) {

            detectionList.textContent =
                error.message;

        }

    }

    finally {

        if (analyzeButton) {

            analyzeButton.disabled =
                false;

        }

    }

}


/* =====================================================
   CLEAR IMAGE
   ===================================================== */

function clearSelectedImage() {

    selectedImage =
        null;


    const imageInput =
        document.getElementById(
            "imageInput"
        );

    const analyzedImage =
        document.getElementById(
            "analyzedImage"
        );

    const placeholder =
        document.getElementById(
            "uploadPlaceholder"
        );

    const status =
        document.getElementById(
            "analysisStatus"
        );

    const detectionCount =
        document.getElementById(
            "imageDetectionCount"
        );

    const detectionList =
        document.getElementById(
            "imageDetectionList"
        );

    const analyzeButton =
        document.getElementById(
            "analyzeImageButton"
        );

    const clearButton =
        document.getElementById(
            "clearImageButton"
        );


    if (imageInput) {

        imageInput.value =
            "";

    }


    if (analyzedImage) {

        analyzedImage.src =
            "";

        analyzedImage.style.display =
            "none";

    }


    if (placeholder) {

        placeholder.style.display =
            "block";

    }


    if (status) {

        status.textContent =
            "READY";

    }


    if (detectionCount) {

        detectionCount.textContent =
            "Objects Detected: 0";

    }


    if (detectionList) {

        detectionList.textContent =
            "No image analyzed yet.";

    }


    if (analyzeButton) {

        analyzeButton.disabled =
            true;

    }


    if (clearButton) {

        clearButton.disabled =
            true;

    }

}