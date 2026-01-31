from google import genai
from google.genai import types
import base64
from typing import List, Optional
from PIL import Image
import io
import os
import uuid
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.garden_design import GardenDesign
from app.core.config import settings


# ============ Plants Data (Indonesian names, English prompts) ============
PLANTS_FOR_GENERATE = [
    # Sayuran Daun (Leafy Vegetables)
    {"id": "lettuce", "name": "Selada", "category": "leafy_vegetables", "prompt_name": "lettuce"},
    {"id": "spinach", "name": "Bayam", "category": "leafy_vegetables", "prompt_name": "spinach"},
    {"id": "pak_choi", "name": "Pak Choi", "category": "leafy_vegetables", "prompt_name": "pak choi"},
    {"id": "kale", "name": "Kale", "category": "leafy_vegetables", "prompt_name": "kale"},
    
    # Sayuran Buah (Fruit Vegetables)
    {"id": "tomato", "name": "Tomat", "category": "fruit_vegetables", "prompt_name": "tomato plant with tomatoes"},
    {"id": "chili_pepper", "name": "Cabai", "category": "fruit_vegetables", "prompt_name": "chili pepper plant"},
    {"id": "bell_pepper", "name": "Paprika", "category": "fruit_vegetables", "prompt_name": "bell pepper plant"},
    {"id": "strawberry", "name": "Stroberi", "category": "fruit_vegetables", "prompt_name": "strawberry plant"},
    
    # Rempah (Herbs)
    {"id": "basil", "name": "Kemangi", "category": "herbs", "prompt_name": "basil herb"},
    {"id": "mint", "name": "Mint", "category": "herbs", "prompt_name": "mint herb"},
    {"id": "lemongrass", "name": "Serai", "category": "herbs", "prompt_name": "lemongrass"},
    {"id": "coriander", "name": "Ketumbar", "category": "herbs", "prompt_name": "coriander herb"},
    
    # Tanaman Obat (Medicinal Plants)
    {"id": "ginger", "name": "Jahe", "category": "medicinal_plants", "prompt_name": "ginger plant"},
    {"id": "turmeric", "name": "Kunyit", "category": "medicinal_plants", "prompt_name": "turmeric plant"},
    {"id": "aloe_vera", "name": "Lidah Buaya", "category": "medicinal_plants", "prompt_name": "aloe vera"},
    {"id": "kumis_kucing", "name": "Kumis Kucing", "category": "medicinal_plants", "prompt_name": "cat's whiskers plant"},
]

# ============ Design Styles Data (Indonesian names, English prompts) ============
DESIGN_STYLES = [
    {
        "id": "minimalist",
        "name": "Taman Vertikal Minimalis",
        "description": "Clean layout with neutral colors, simple modular planters, and balanced spacing"
    },
    {
        "id": "modern",
        "name": "Pertanian Urban Modern",
        "description": "Sleek metal frames, contemporary vertical racks, organized and efficient layout"
    },
    {
        "id": "industrial",
        "name": "Taman Dinding Industrial",
        "description": "Exposed metal structures, dark or concrete tones, urban warehouse aesthetic"
    },
    {
        "id": "natural",
        "name": "Dinding Hijau Natural",
        "description": "Dense foliage, organic and irregular plant arrangement, lush and fresh appearance"
    },
    {
        "id": "hydroponic",
        "name": "Sistem Dinding Hidroponik",
        "description": "PVC pipes or hydroponic modules, clean and functional layout, soil-less planting"
    },
    {
        "id": "diy",
        "name": "Urban Farming DIY Hemat Biaya",
        "description": "Simple or recycled materials, practical and affordable design, community-friendly"
    },
]

# ============ Style Prompt Mappings (English) ============
STYLE_MAP = {
    "minimalist": """
Minimalist Vertical Garden Style:
- Clean, organized layout
- Neutral colors (whites, grays, blacks)
- Simple modular planters
- Balanced and symmetrical spacing
- Minimalist metal or wooden frames
- Modern and sleek appearance
""",
    "modern": """
Modern Urban Farming Style:
- Sleek metal frames and structures
- Contemporary vertical racks
- Organized and efficient layout
- Clean lines and modern aesthetics
- Professional and polished appearance
- Suitable for modern residential spaces
""",
    "industrial": """
Industrial Wall Garden Style:
- Exposed metal structures
- Dark tones and concrete elements
- Urban warehouse aesthetic
- Raw and rustic appearance
- Heavy-duty materials (steel, iron)
- Bold and striking design
""",
    "natural": """
Natural Green Wall Style:
- Dense foliage and lush greenery
- Organic and irregular plant arrangement
- Natural color palette (greens, browns, earth tones)
- Soft and welcoming appearance
- Natural growing pattern
- Fresh and vibrant look
""",
    "hydroponic": """
Hydroponic Wall System:
- PVC pipes or modern hydroponic modules
- Clean and functional layout
- Soil-less planting system
- Technical and organized appearance
- Modern water flow systems visible
- High-tech and efficient design
""",
    "diy": """
DIY Low-Budget Urban Farming Style:
- Simple and recycled materials
- Practical and affordable design
- Creative and community-friendly appearance
- Rustic charm with functional design
- Repurposed containers and materials
- Accessible and approachable aesthetic
""",
}

# ============ Plant Name Mapping for Prompts (English) ============
PLANT_NAMES = {
    "lettuce": "lettuce",
    "spinach": "spinach",
    "pak_choi": "pak choi",
    "kale": "kale",
    "tomato": "tomato plant with tomatoes",
    "chili_pepper": "chili pepper plant",
    "bell_pepper": "bell pepper plant",
    "strawberry": "strawberry plant",
    "basil": "basil herb",
    "mint": "mint herb",
    "lemongrass": "lemongrass",
    "coriander": "coriander herb",
    "ginger": "ginger plant",
    "turmeric": "turmeric plant",
    "aloe_vera": "aloe vera",
    "kumis_kucing": "cat's whiskers plant",
}


class GardenDesignService:
    """Service for garden design generation using Gemini AI"""
    
    @staticmethod
    def get_plants_for_generate() -> List[dict]:
        """Get all plants available for garden design generation"""
        return PLANTS_FOR_GENERATE
    
    @staticmethod
    def get_design_styles() -> List[dict]:
        """Get all design styles available for garden design generation"""
        return DESIGN_STYLES
    
    @staticmethod
    def build_prompt(plants: List[str], style: str) -> tuple[str, str]:
        """
        Build positive and negative prompts for image generation
        
        Args:
            plants: List of plant IDs
            style: Design style ID
            
        Returns:
            Tuple of (positive_prompt, negative_prompt)
        """
        # Convert plant IDs to human-readable names
        plant_names = [PLANT_NAMES.get(plant_id, plant_id) for plant_id in plants]
        plant_list = ", ".join(plant_names)
        
        # Get style description
        style_description = STYLE_MAP.get(style, STYLE_MAP["minimalist"])
        
        # Build positive prompt
        positive_prompt = f"""Transform the uploaded photo of a plain wall into a realistic urban farming design covering the 80% WALL.

Style:
{style_description}

Requirements:
- Keep the original wall structure, perspective, lighting, and environment.
- COMPLETELY COVER THE WALL with urban farming installation from top to bottom, left to right.
- The vertical garden should fill the 80% visible wall surface (at least 80-90% coverage).
- Create a VARIED and DYNAMIC layout with different planting module sizes and arrangements.
- Mix different installation styles: hanging planters, mounted shelves, wall-mounted pockets, tiered structures, and climbing elements.
- Create visual interest with varying heights, depths, and plant sizes.
- Use realistic materials appropriate to the selected style.
- Plants to include: {plant_list}.
- The plants should look healthy, green, lush, and naturally growing with varied leaf shapes and colors.
- Create a DENSE, FULL COVERAGE vertical garden installation.
- Plants should be abundant, overflowing, and naturally cascading with organic arrangement.
- Avoid repetitive rows/columns - instead create an artistic, flowing composition.
- Mix planted areas with small spaces for visual breathing room.
- Suitable for a small urban residential environment.
- Modern, clean, and practical design with creative arrangement.
- High realism, photorealistic style.
- Do not change the surrounding area except for the farming elements.
- Professional and realistic rendering.
- Good lighting that matches the original photo.
- The wall should look like a thriving, vibrant, and creatively-designed urban farming space."""

        # Negative prompt
        negative_prompt = """Avoid:
- cartoon or illustration style
- fantasy or sci-fi elements
- unrealistic colors
- people or animals
- text, logos, or watermarks
- blurry or low quality
- distorted proportions
- unnatural looking plants
- sparse or empty planting spaces
- incomplete wall coverage
- small or minimal farming installations
- bare wall showing through excessively"""

        return positive_prompt, negative_prompt

    @staticmethod
    async def generate_image(
        image_base64: str,
        plants: List[str],
        style: str,
        api_key: str
    ) -> str:
        """
        Generate urban farming wall design using Gemini Image Generation API
        
        Args:
            image_base64: Base64 encoded input image
            plants: List of selected plant IDs
            style: Design style ID
            api_key: Gemini API key
            
        Returns:
            Base64 encoded generated image
        """
        # Initialize Gemini client
        client = genai.Client(api_key=api_key)
        
        # Build prompts
        positive_prompt, negative_prompt = GardenDesignService.build_prompt(plants, style)
        
        # Clean base64 string
        clean_base64 = image_base64.split(",")[-1] if "," in image_base64 else image_base64
        image_data = base64.b64decode(clean_base64)
        
        # Load original image
        original_img = Image.open(io.BytesIO(image_data))
        
        # Build comprehensive prompt for image generation
        full_prompt = f"""Transform this wall image into a realistic urban farming wall design.

{positive_prompt}

{negative_prompt}

Create a photorealistic transformation of the wall with urban farming elements while maintaining the original wall structure, lighting, and perspective."""
        
        # Generate image using Gemini 2.5 Flash Image model (supports image-to-image)
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[full_prompt, original_img],
        )
        
        # Extract generated image from response - correct structure
        if hasattr(response, 'candidates') and response.candidates:
            for candidate in response.candidates:
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            # Check for text response
                            if hasattr(part, 'text') and part.text:
                                print(f"AI Response: {part.text}")
                            # Check for inline image data
                            if hasattr(part, 'inline_data') and part.inline_data is not None:
                                # Get image bytes directly from inline_data
                                if hasattr(part.inline_data, 'data'):
                                    image_bytes = part.inline_data.data
                                else:
                                    # Try to get data as bytes
                                    image_bytes = bytes(part.inline_data)
                                
                                # Convert image bytes to PIL Image then to base64
                                try:
                                    generated_image = Image.open(io.BytesIO(image_bytes))
                                    buffered = io.BytesIO()
                                    generated_image.save(buffered, format="PNG")
                                    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                                    return f"data:image/png;base64,{img_base64}"
                                except Exception as img_error:
                                    # If can't convert to image, try direct base64 encoding
                                    img_base64 = base64.b64encode(image_bytes).decode('utf-8')
                                    mime_type = getattr(part.inline_data, 'mime_type', 'image/png')
                                    return f"data:{mime_type};base64,{img_base64}"
        
        # If no image generated, raise exception with more info
        raise Exception(f"Failed to generate image. Response structure: {type(response)}")
    
    @staticmethod
    def save_image_to_file(image_base64: str, folder: str, prefix: str = "") -> str:
        """
        Save base64 image to file and return the file path
        
        Args:
            image_base64: Base64 encoded image
            folder: Subfolder within UPLOAD_DIR (inputs or outputs)
            prefix: Optional prefix for filename
            
        Returns:
            Relative file path
        """
        # Clean base64 string and determine mime type
        if "," in image_base64:
            header, clean_base64 = image_base64.split(",", 1)
            if "png" in header:
                extension = "png"
            elif "jpeg" in header or "jpg" in header:
                extension = "jpg"
            else:
                extension = "png"
        else:
            clean_base64 = image_base64
            extension = "png"
        
        # Decode image
        image_data = base64.b64decode(clean_base64)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{prefix}_{timestamp}_{unique_id}.{extension}" if prefix else f"{timestamp}_{unique_id}.{extension}"
        
        # Create full path
        upload_dir = settings.UPLOAD_DIR
        full_folder_path = os.path.join(upload_dir, folder)
        os.makedirs(full_folder_path, exist_ok=True)
        
        file_path = os.path.join(full_folder_path, filename)
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(image_data)
        
        # Return relative path for URL (remove 'public/' prefix)
        url_path = file_path.replace("public/", "")
        return f"/{url_path}"
    
    @staticmethod
    def create_garden_design(
        db: Session,
        user_id: int,
        name: Optional[str],
        input_photo_url: str,
        output_photo_url: str,
        preferences: dict
    ) -> GardenDesign:
        """
        Create a new garden design record in database
        
        Args:
            db: Database session
            user_id: User ID
            name: Optional design name
            input_photo_url: URL to input photo
            output_photo_url: URL to output photo
            preferences: Design preferences (plants, style)
            
        Returns:
            Created GardenDesign object
        """
        garden_design = GardenDesign(
            user_id=user_id,
            name=name,
            input_photo_url=input_photo_url,
            preferences=preferences,
            design_output=output_photo_url
        )
        
        db.add(garden_design)
        db.commit()
        db.refresh(garden_design)
        
        return garden_design
    
    @staticmethod
    def get_user_design_history(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[GardenDesign], int]:
        """
        Get garden design history for a user
        
        Args:
            db: Database session
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple of (list of designs, total count)
        """
        query = db.query(GardenDesign).filter(GardenDesign.user_id == user_id)
        total = query.count()
        designs = query.order_by(GardenDesign.created_at.desc()).offset(skip).limit(limit).all()
        
        return designs, total
    
    @staticmethod
    def get_design_by_id(db: Session, design_id: int, user_id: int) -> Optional[GardenDesign]:
        """
        Get a specific garden design by ID
        
        Args:
            db: Database session
            design_id: Design ID
            user_id: User ID (for authorization)
            
        Returns:
            GardenDesign object or None
        """
        return db.query(GardenDesign).filter(
            GardenDesign.id == design_id,
            GardenDesign.user_id == user_id
        ).first()
