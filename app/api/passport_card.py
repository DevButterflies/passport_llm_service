import io
import logging
import time
from PIL import Image, UnidentifiedImageError

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, Summary, generate_latest, CONTENT_TYPE_LATEST
from app.models.combined import PassportCardResponse
from app.config import MAX_HEIGHT, MAX_WIDTH, PROMPT_PASSPORT, PV_PATH
from app.utils.prompt_utils import resize_passport_card_image, save_pv
from app.api import llm 

logger = logging.getLogger(__name__)
router = APIRouter()


# Prometheus metrics
REQUEST_COUNT = Counter("passport_card_requests_total", "Total Passport card requests", ["status"])
REQUEST_LATENCY = Summary("passport_card_request_latency_seconds", "Latency of /passport_card requests in seconds")
ERROR_COUNT = Counter("passport_card_errors_total", "Total Passport card errors", ["error_type"])


@router.post("/passport_card")
async def passport_card(request: Request, photo: UploadFile = File(None)):
    start = time.time()
    logger.info("[API] /passport_card called")

    try:
        if not photo :
            ERROR_COUNT.labels(error_type="missing_image").inc()
            REQUEST_COUNT.labels(status="error").inc()
            raise HTTPException(status_code=400, detail="At least one image is required.")

        try:
            passport = Image.open(io.BytesIO(await photo.read())) 
        except UnidentifiedImageError:
            logger.warning("[WARN] Invalid image. Using dummy.")
            ERROR_COUNT.labels(error_type="invalid_passport_image").inc()
            raise HTTPException(status_code=400, detail="photo must be a valid image file.")

        except Exception as e:
            logger.warning(f"[WARN] Front image error: {e}. Using dummy.")
            ERROR_COUNT.labels(error_type="front_image_error").inc()
            raise HTTPException(status_code=400, detail="Error processing the image.")




        #---------------------------------------------------------------------
        #---------------------------------------------------------------------    


        pass_resized = resize_passport_card_image(passport, MAX_WIDTH, MAX_HEIGHT)

        result_with_pv = await llm.process_task_async(
            [PROMPT_PASSPORT, pass_resized],
            PassportCardResponse
        )

        if result_with_pv.get("status") == "error":
            ERROR_COUNT.labels(error_type="llm_error").inc()
            REQUEST_COUNT.labels(status="error").inc()
            logger.warning(f"[LLM] LLM processing failed: {result_with_pv.get('error_msg')}")
            ERROR_COUNT.labels(error_type="unexpected_error").inc()
            raise HTTPException(
                status_code=500,
                detail="An error occurred during LLM processing. Please try again later."
            )

        try:
            save_pv("passport", result_with_pv["pv"], save_dir=PV_PATH)
        except Exception as e:
            logger.warning(f"[PV] Failed to save prompt-value log: {e}")
            ERROR_COUNT.labels(error_type="pv_save_error").inc()

        duration = time.time() - start
        REQUEST_COUNT.labels(status="success").inc()
        REQUEST_LATENCY.observe(duration)

        return {
            "data": result_with_pv["result"].model_dump(),
            "audit": result_with_pv["pv"],
            "duration": str(duration)
        }

    except HTTPException:
        raise
    except Exception as e:
        ERROR_COUNT.labels(error_type="unexpected_error").inc()
        REQUEST_COUNT.labels(status="error").inc()
        logger.error(f"[SERVER] Unexpected error in /passport: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred during processing. Please try again later."
        )

@router.get("/metrics")
async def metrics():
    data = generate_latest()
    return PlainTextResponse(data, media_type=CONTENT_TYPE_LATEST)
