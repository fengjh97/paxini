# Japanese Hotel / Ryokan / Minshuku Website Design Research Report

**Date:** March 4, 2026
**Purpose:** Comprehensive design research for creating a professional Japanese hospitality website

---

## Table of Contents

1. [Website Sections & Structure](#1-website-sections--structure)
2. [Design Trends 2025-2026](#2-design-trends-2025-2026)
3. [Color Palettes](#3-color-palettes)
4. [Typography & Font Pairings](#4-typography--font-pairings)
5. [Must-Have Features](#5-must-have-features)
6. [Image & Asset Needs](#6-image--asset-needs)
7. [UX Best Practices](#7-ux-best-practices)
8. [Reference Websites](#8-reference-websites)
9. [Sources](#9-sources)

---

## 1. Website Sections & Structure

A top-tier Japanese hotel, ryokan, or minshuku (民宿) website should include the following sections. The navigation should be clean and shallow -- guests should reach any key page within 1-2 clicks from anywhere on the site.

### 1.1 Primary Navigation Sections

| Section | Japanese | Description |
|---------|----------|-------------|
| **Home / Top** | トップ | Hero imagery, seasonal messaging, quick booking widget, brand introduction |
| **Rooms** | 客室 (きゃくしつ) | Room types with photos, floor plans, amenities list, tatami/Western options |
| **Dining** | お食事 (おしょくじ) | Kaiseki (懐石) multi-course meals, breakfast, seasonal menus, local ingredients |
| **Onsen / Bath** | 温泉・お風呂 | Hot spring descriptions, indoor/outdoor baths, private baths (貸切風呂), bathing etiquette |
| **Facilities** | 館内施設 | Garden (庭園), lobby, lounge, gift shop, spa, fitness, common areas |
| **Access** | アクセス | Directions by car/train/bus/air, interactive map, shuttle service, parking |
| **Reservation** | ご予約 | Online booking engine, plan selection, calendar availability |
| **Gallery** | ギャラリー | Photo and video gallery organized by category |

### 1.2 Secondary Navigation / Footer Sections

| Section | Japanese | Description |
|---------|----------|-------------|
| **Seasonal Events** | 季節のご案内 | Cherry blossom, autumn foliage, snow scenes, festivals, seasonal activities |
| **Experience** | 過ごし方 | Day-in-the-life guide, cultural activities (tea ceremony, yukata), local excursions |
| **About / History** | 当館について | Inn history, philosophy, omotenashi (おもてなし) spirit, owner/family story |
| **FAQ** | よくある質問 | Check-in/out times, cancellation policy, children, pets, payment |
| **News / Blog** | お知らせ | Updates, seasonal announcements, media features |
| **Guest Reviews** | お客様の声 | Testimonials, review aggregation from major platforms |
| **Privacy Policy** | プライバシーポリシー | Legal compliance, cookie policy |
| **Language Switcher** | 言語切替 | Japanese, English, Chinese (Simplified/Traditional), Korean at minimum |

### 1.3 Recommended Page Flow (Sitemap)

```
Home
├── Rooms
│   ├── Room Type A (e.g., Japanese Suite / 和室特別室)
│   ├── Room Type B (e.g., Standard Japanese / 和室)
│   ├── Room Type C (e.g., Western-Japanese / 和洋室)
│   └── Room Comparison Table
├── Dining
│   ├── Kaiseki Dinner / 夕食
│   ├── Breakfast / 朝食
│   └── Special Dietary Options
├── Onsen / Bath
│   ├── Large Public Bath / 大浴場
│   ├── Open-Air Bath / 露天風呂
│   └── Private Bath / 貸切風呂
├── Facilities & Grounds
│   ├── Garden / 庭園
│   ├── Lobby & Lounge
│   └── Amenities List
├── Experience & Activities
│   ├── How to Spend Your Stay / 過ごし方
│   ├── Seasonal Highlights / 季節の魅力
│   └── Local Attractions / 周辺観光
├── Access & Transportation
├── Reservation / Booking
│   ├── Room Plans & Rates
│   └── Availability Calendar
├── Gallery
├── About Us / History
├── News
├── FAQ
└── Contact
```

---

## 2. Design Trends 2025-2026

### 2.1 Zen Minimalism & Ma (間) -- Negative Space

The dominant trend for luxury Japanese hospitality sites is **zen minimalism** -- generous whitespace (or "ma"), restrained color palettes, and deliberate pacing. Inspired by the concept of 間 (ma, meaning "space" or "pause"), the design allows the visitor to breathe between content sections.

**Key characteristics:**
- Ample whitespace between sections (100-200px+ vertical spacing)
- Limited color palette (2-3 colors maximum)
- Slow, meditative scroll pacing
- Content revealed gradually, not all at once
- Reference: Hoshinoya and Aman hotel sites exemplify this approach

### 2.2 Full-Bleed Photography & Cinematic Hero Sections

Large, immersive photography dominates the viewport. The hero section is typically a full-screen image or video that immediately communicates the atmosphere.

**Implementation:**
- Full-viewport hero images (100vh) with minimal text overlay
- Autoplay ambient video backgrounds (muted, subtle motion -- steam rising from onsen, garden in wind)
- Image sections that span the full browser width with no margins
- Vertical photography optimized for mobile-first viewing

### 2.3 Parallax & Scroll-Triggered Animations

Parallax scrolling creates depth and dimensionality. Elements move at different speeds as the user scrolls, making the experience feel layered and immersive.

**2025-2026 approach:**
- Subtle parallax (background moves 10-20% slower, not aggressively)
- Scroll-triggered fade-ins, lateral slides, and reveals
- Kinetic typography that animates on scroll
- Scroll progress indicators tying into seasonal themes

### 2.4 Vertical Text (Tategaki / 縦書き)

Traditional Japanese vertical writing (縦書き) is a distinctive design element that signals authenticity and cultural depth.

**Usage recommendations:**
- Section headers or short poetic phrases in vertical orientation
- Decorative accent alongside horizontal body text
- CSS `writing-mode: vertical-rl` implementation
- Use sparingly -- 1-2 instances per page for accent, not for main content

### 2.5 Bento Box Layout (Grid Composition)

Inspired by the orderly, modular compartments of a bento box, this layout approach uses asymmetric grids where content is neatly organized but visually dynamic.

**Implementation:**
- CSS Grid with varying column/row spans
- Mixed media (photo + text + small detail image) in one grid
- Works well for room comparison, facility overview, and gallery pages

### 2.6 Glassmorphism & Soft Material Design

Semi-transparent "frosted glass" cards that overlay photographs, creating depth while maintaining readability.

**Implementation:**
- `backdrop-filter: blur(10px)` with semi-transparent backgrounds
- Subtle shadows and rounded corners
- Works well for booking widgets overlaying hero images
- Neumorphic buttons with soft press effects

### 2.7 AI-Driven Personalization (Omotenashi Digital)

Reflecting the Japanese hospitality spirit of omotenashi (おもてなし), websites are integrating subtle AI personalization:

- Auto-detecting browser language and locale
- Time-of-day theme adjustments (softer tones at night)
- Seasonal content rotation based on actual calendar date
- Personalized room/plan recommendations based on browsing behavior

### 2.8 Micro-Interactions & Attention to Detail

Just as ryokan hospitality focuses on details, the website should include thoughtful micro-interactions:

- Hover effects on room cards revealing a secondary image
- Smooth page transitions (crossfade between pages)
- Custom cursor changes when hovering over interactive elements
- Loading animations themed to the property (e.g., falling sakura petals)

---

## 3. Color Palettes

Below are four curated palettes rooted in Japanese aesthetic traditions, each with specific hex codes and usage guidance.

### 3.1 Palette A: Wabi-Sabi Earth Tones (侘寂)

Inspired by the beauty of imperfection, natural aging, and organic materials. This palette feels warm, grounded, and serene.

| Role | Color Name | Hex Code | Usage |
|------|-----------|----------|-------|
| **Background** | Shiro-neri (白練) -- Unbleached White | `#F5F0E8` | Page backgrounds, card backgrounds |
| **Surface** | Kitsune-iro (狐色) -- Tatami Beige | `#D4C5A9` | Secondary surfaces, dividers, borders |
| **Primary Text** | Sumi (墨) -- Ink | `#2B2520` | Headings, body text |
| **Accent 1** | Tobi-iro (鳶色) -- Rust Brown | `#7B4B3A` | Buttons, links, highlights |
| **Accent 2** | Rikyuu-cha (利休茶) -- Moss Sage | `#897D5A` | Secondary accents, tags, subtle details |
| **Accent 3** | Kuri-iro (栗色) -- Chestnut | `#6A3B2F` | Hover states, active elements |
| **Light Accent** | Sakura-nezumi (桜鼠) -- Dusty Rose | `#C8A2A2` | Subtle highlights, seasonal accents |

**CSS Custom Properties:**
```css
:root {
  --color-bg: #F5F0E8;
  --color-surface: #D4C5A9;
  --color-text: #2B2520;
  --color-accent: #7B4B3A;
  --color-accent-secondary: #897D5A;
  --color-accent-dark: #6A3B2F;
  --color-highlight: #C8A2A2;
}
```

**Best for:** Rustic minshuku, mountain ryokan, properties emphasizing nature and tradition.

---

### 3.2 Palette B: Zen White & Stone Grey (禅)

A restrained, almost monochromatic palette that places full emphasis on photography and content. Inspired by Zen rock gardens (枯山水) and calligraphy.

| Role | Color Name | Hex Code | Usage |
|------|-----------|----------|-------|
| **Background** | Gofun (胡粉) -- Chalk White | `#FAFAF7` | Page background |
| **Surface** | Hai (灰) -- Ash Grey | `#E8E4DE` | Section backgrounds, cards |
| **Border/Line** | Nezumi (鼠) -- Stone Grey | `#9E9E93` | Dividers, borders, subtle text |
| **Primary Text** | Kuro (黒) -- Sumi Black | `#1A1A18` | Headings, primary content |
| **Secondary Text** | Nibi (鈍) -- Dull Grey | `#5C5C58` | Captions, metadata, secondary info |
| **Accent** | Shu (朱) -- Vermillion Red | `#C14B3D` | Call-to-action buttons, key links |
| **Accent 2** | Matcha (抹茶) -- Tea Green | `#7B8B6F` | Seasonal accents, nature elements |

**CSS Custom Properties:**
```css
:root {
  --color-bg: #FAFAF7;
  --color-surface: #E8E4DE;
  --color-border: #9E9E93;
  --color-text: #1A1A18;
  --color-text-secondary: #5C5C58;
  --color-accent: #C14B3D;
  --color-accent-secondary: #7B8B6F;
}
```

**Best for:** High-end ryokan, contemporary Japanese design, properties with stunning photography to showcase.

---

### 3.3 Palette C: Modern Luxury Dark (墨夜)

A sophisticated dark palette with gold accents, suitable for luxury properties that want a premium, exclusive feel. Inspired by the interplay of sumi ink, lacquerware, and gold leaf (金箔).

| Role | Color Name | Hex Code | Usage |
|------|-----------|----------|-------|
| **Background** | Kuro-tsuchi (黒土) -- Dark Earth | `#1C1B19` | Page background |
| **Surface** | Ro (呂) -- Lacquer Black | `#2A2826` | Cards, elevated surfaces |
| **Border** | Hai-iro (灰色) -- Charcoal | `#3D3B38` | Borders, subtle dividers |
| **Primary Text** | Shiro (白) -- Pure White | `#F2F0EB` | Headings, primary text |
| **Secondary Text** | Gin (銀) -- Silver | `#A8A49E` | Secondary text, captions |
| **Accent 1** | Kin (金) -- Gold | `#C9A96E` | Buttons, highlights, key links |
| **Accent 2** | Shu (朱) -- Deep Vermillion | `#9B3A2E` | Hover states, warnings, secondary CTA |

**CSS Custom Properties:**
```css
:root {
  --color-bg: #1C1B19;
  --color-surface: #2A2826;
  --color-border: #3D3B38;
  --color-text: #F2F0EB;
  --color-text-secondary: #A8A49E;
  --color-accent: #C9A96E;
  --color-accent-secondary: #9B3A2E;
}
```

**Best for:** Luxury resort ryokan, exclusive onsen retreats, high-end boutique properties.

---

### 3.4 Palette D: Traditional Indigo & Natural (藍染)

Inspired by Japanese indigo dyeing (藍染め), washi paper, and the natural tones found in traditional interiors. This palette has strong cultural identity.

| Role | Color Name | Hex Code | Usage |
|------|-----------|----------|-------|
| **Background** | Torinoko (鳥の子) -- Eggshell / Washi | `#F0E6D3` | Page background |
| **Surface** | Kaya (萱) -- Reed Beige | `#E0D5C0` | Cards, secondary areas |
| **Primary Text** | Kon (紺) -- Deep Indigo | `#1B2D4E` | Headings, primary text |
| **Secondary Text** | Ai-nezumi (藍鼠) -- Blue Grey | `#4A5568` | Secondary text, metadata |
| **Accent 1** | Ai (藍) -- Indigo Blue | `#2C5F7C` | Links, buttons, key elements |
| **Accent 2** | Kincha (金茶) -- Golden Brown | `#C18A40` | Secondary accents, highlights |
| **Highlight** | Ben (紅) -- Crimson | `#B33B3B` | Call-to-action, alerts |

**CSS Custom Properties:**
```css
:root {
  --color-bg: #F0E6D3;
  --color-surface: #E0D5C0;
  --color-text: #1B2D4E;
  --color-text-secondary: #4A5568;
  --color-accent: #2C5F7C;
  --color-accent-gold: #C18A40;
  --color-cta: #B33B3B;
}
```

**Best for:** Properties with strong cultural heritage, traditional architecture, indigo-dyeing regions (Tokushima, etc.), historic ryokan.

---

## 4. Typography & Font Pairings

### 4.1 Understanding Japanese Typography Categories

| Japanese Term | Western Equivalent | Character | Use Case |
|---------------|-------------------|-----------|----------|
| **明朝体 (Mincho-tai)** | Serif | Elegant, formal, literary | Headings, luxury brands, traditional feel |
| **ゴシック体 (Gothic-tai)** | Sans-serif | Modern, clean, functional | Body text, UI elements, modern brands |
| **丸ゴシック体 (Maru Gothic)** | Rounded sans-serif | Friendly, warm, approachable | Casual content, minshuku, family-oriented |

### 4.2 Recommended Font Pairings (All Available on Google Fonts)

#### Pairing 1: Classic Elegance (Best for Luxury Ryokan)

| Role | Japanese Font | English Font | Weights |
|------|--------------|--------------|---------|
| **Headings** | Shippori Mincho (`Shippori Mincho`) | Cormorant Garamond (`Cormorant Garamond`) | 500, 700 |
| **Body** | Noto Sans JP (`Noto Sans JP`) | Source Sans 3 (`Source Sans 3`) | 300, 400, 600 |

```css
/* Classic Elegance */
@import url('https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@500;700&family=Cormorant+Garamond:wght@500;700&family=Noto+Sans+JP:wght@300;400;600&family=Source+Sans+3:wght@300;400;600&display=swap');

h1, h2, h3 {
  font-family: 'Shippori Mincho', 'Cormorant Garamond', serif;
}
body, p {
  font-family: 'Noto Sans JP', 'Source Sans 3', sans-serif;
}
```

**Character:** Refined, literary, steeped in tradition. The Mincho strokes echo calligraphy while Cormorant Garamond provides matching high-contrast elegance in English. Best paired with Palettes A or D.

---

#### Pairing 2: Contemporary Zen (Best for Modern Boutique)

| Role | Japanese Font | English Font | Weights |
|------|--------------|--------------|---------|
| **Headings** | Zen Kaku Gothic New (`Zen Kaku Gothic New`) | Playfair Display (`Playfair Display`) | 400, 700 |
| **Body** | Noto Sans JP (`Noto Sans JP`) | Inter (`Inter`) | 300, 400, 500 |

```css
/* Contemporary Zen */
@import url('https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;700&family=Playfair+Display:wght@400;700&family=Noto+Sans+JP:wght@300;400;500&family=Inter:wght@300;400;500&display=swap');

h1, h2, h3 {
  font-family: 'Zen Kaku Gothic New', 'Playfair Display', serif;
}
body, p {
  font-family: 'Noto Sans JP', 'Inter', sans-serif;
}
```

**Character:** Clean geometric Japanese meets editorial English serif. A blend of contemporary and classic that feels design-forward without losing warmth. Best paired with Palettes B or C.

---

#### Pairing 3: Warm & Approachable (Best for Minshuku / Family Inn)

| Role | Japanese Font | English Font | Weights |
|------|--------------|--------------|---------|
| **Headings** | Zen Maru Gothic (`Zen Maru Gothic`) | Lora (`Lora`) | 400, 700 |
| **Body** | Zen Maru Gothic (`Zen Maru Gothic`) | Nunito (`Nunito`) | 300, 400, 600 |

```css
/* Warm & Approachable */
@import url('https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@300;400;700&family=Lora:wght@400;700&family=Nunito:wght@300;400;600&display=swap');

h1, h2, h3 {
  font-family: 'Zen Maru Gothic', 'Lora', serif;
}
body, p {
  font-family: 'Zen Maru Gothic', 'Nunito', sans-serif;
}
```

**Character:** The rounded corners of Zen Maru Gothic convey warmth and friendliness, matching the intimate atmosphere of a family-run minshuku. Lora adds gentle elegance to English headings. Best paired with Palette A.

---

#### Pairing 4: Luxe Minimal (Best for Dark Theme / Premium)

| Role | Japanese Font | English Font | Weights |
|------|--------------|--------------|---------|
| **Headings** | Noto Serif JP (`Noto Serif JP`) | EB Garamond (`EB Garamond`) | 400, 600 |
| **Body** | Noto Sans JP (`Noto Sans JP`) | Montserrat (`Montserrat`) | 300, 400, 500 |

```css
/* Luxe Minimal */
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;600&family=EB+Garamond:wght@400;600&family=Noto+Sans+JP:wght@300;400;500&family=Montserrat:wght@300;400;500&display=swap');

h1, h2, h3 {
  font-family: 'Noto Serif JP', 'EB Garamond', serif;
}
body, p {
  font-family: 'Noto Sans JP', 'Montserrat', sans-serif;
}
```

**Character:** Noto Serif JP ensures cross-script harmony and comprehensive glyph coverage. EB Garamond is a timeless humanist serif for English. Clean and universally elegant. Best paired with Palette C.

---

### 4.3 Typography Best Practices for Japanese Hospitality Sites

- **Line height:** Japanese text reads best at `line-height: 1.8` to `2.0` (more generous than English)
- **Font size:** Minimum 16px for body text; 14px minimum on mobile
- **Letter spacing:** Japanese characters at `letter-spacing: 0.05em` to `0.1em` for headings for an open, luxurious feel
- **Vertical text CSS:** Use `writing-mode: vertical-rl; text-orientation: mixed;` for decorative vertical elements
- **Mixed-language fallback:** Always stack Japanese fonts first, then English, then generic: `font-family: 'Noto Sans JP', 'Inter', sans-serif;`
- **Font loading:** Use `display=swap` in Google Fonts imports to prevent layout shift (FOUT over FOIT)
- **Weight usage:** Keep to 2-3 weights per family to reduce load time

---

## 5. Must-Have Features

### 5.1 Reservation & Booking System

| Feature | Priority | Description |
|---------|----------|-------------|
| **Integrated Booking Widget** | Critical | Embedded on homepage and header; should not redirect to external site |
| **Availability Calendar** | Critical | Visual calendar showing open/closed dates with color coding |
| **Plan-Based Selection** | Critical | Japanese hotel booking convention: guests select "plans" (e.g., "2 meals + room") rather than just rooms |
| **Rate Transparency** | Critical | Show total price including tax/service charge upfront; no surprises at checkout |
| **Guest Count Selector** | High | Adults, children (with age ranges), infants |
| **Special Requests** | High | Dietary restrictions, celebration occasions, accessibility needs |
| **Confirmation Email** | Critical | Automated bilingual confirmation with reservation details |
| **Cancellation Policy** | High | Clear, visible cancellation terms before booking |
| **Payment Options** | High | Credit card, PayPay, LINE Pay, bank transfer (for domestic guests) |

### 5.2 Photo Gallery

| Feature | Priority | Description |
|---------|----------|-------------|
| **Category Filtering** | High | Rooms, Dining, Onsen, Garden, Exterior, Seasonal |
| **Lightbox Viewer** | High | Full-screen viewing with swipe navigation |
| **Lazy Loading** | High | Images load as user scrolls to maintain performance |
| **360-Degree Room Views** | Medium | Virtual tour of room interiors |
| **Video Content** | Medium | Short atmospheric videos (30-60 seconds) |

### 5.3 Seasonal Information (季節の案内)

This is a uniquely Japanese feature that international visitors particularly value:

| Season | Japanese | Content |
|--------|----------|---------|
| **Spring** | 春 (haru) | Cherry blossom (桜) schedule, hanami spots, spring kaiseki |
| **Summer** | 夏 (natsu) | Fireworks festivals, river activities, cooling cuisine, fireflies |
| **Autumn** | 秋 (aki) | Autumn foliage (紅葉) peak times, mushroom cuisine, harvest events |
| **Winter** | 冬 (fuyu) | Snow scenery, hot pot (鍋) dining, New Year traditions, ski access |

Implementation: Dynamic banner or section on homepage that auto-rotates based on current date.

### 5.4 Access & Transportation

| Feature | Priority | Description |
|---------|----------|-------------|
| **Interactive Map** | Critical | Google Maps embed with pin location |
| **Multi-Modal Directions** | Critical | From nearest shinkansen station, airport, highway IC |
| **Shuttle/Pickup Service** | High | Times, reservation method, pickup points |
| **Walking Directions** | Medium | From nearest station with photos of landmarks along the way |
| **Local Transportation** | Medium | Bus timetables, taxi info, rental car options |
| **Printable Directions** | Low | PDF download for offline use |

### 5.5 Multilingual Support

| Feature | Priority | Description |
|---------|----------|-------------|
| **Japanese (Primary)** | Critical | Full content in native Japanese |
| **English** | Critical | Complete translation, not machine-translated |
| **Chinese (Simplified)** | High | For mainland China visitors |
| **Chinese (Traditional)** | High | For Taiwan and Hong Kong visitors |
| **Korean** | High | Significant visitor demographic |
| **Language Switcher** | Critical | Display language names in their native script (e.g., "English", "中文", "한국어") |
| **hreflang Tags** | High | Proper SEO for multilingual pages |
| **URL Structure** | High | Subdirectory approach: `/en/`, `/zh/`, `/ko/` |

Accessibility requirements: Set proper `lang` attribute on `<html>` tag, use `lang` attributes on mixed-language content blocks, and ensure WCAG 2.1 AA compliance.

### 5.6 Reviews & Social Proof

| Feature | Priority | Description |
|---------|----------|-------------|
| **Curated Testimonials** | High | Selected guest quotes with attribution |
| **Platform Ratings** | Medium | Display scores from Google, TripAdvisor, Jalan, Rakuten Travel |
| **Photo Reviews** | Medium | Guest-submitted photos with permission |
| **Media Features** | Medium | Press mentions, TV appearances, guidebook features |

### 5.7 Additional Essential Features

| Feature | Priority | Description |
|---------|----------|-------------|
| **SSL Certificate** | Critical | HTTPS for security and trust |
| **Cookie Consent** | Critical | GDPR/privacy compliance |
| **Schema Markup** | High | Hotel structured data for rich search results |
| **Breadcrumb Navigation** | Medium | Orientation aid for deep pages |
| **Social Media Links** | Medium | Instagram (highly visual), LINE (domestic), Facebook |
| **Newsletter Signup** | Low | Email list building for seasonal promotions |

---

## 6. Image & Asset Needs

### 6.1 Complete Photo Shot List

Photography is the single most important design element for a hospitality website. Below is a comprehensive shot list organized by category.

#### Exterior & Architecture (8-12 images)

| Shot | Description | Season/Time | Aspect |
|------|-------------|-------------|--------|
| Hero facade | Full building exterior, best angle | Each season | 16:9, landscape |
| Entrance (genkan) | Welcoming entry with noren curtain | Day + Dusk | 16:9 + 9:16 |
| Garden overview | Full garden from elevated angle | Each season | 16:9, panoramic |
| Garden detail | Close-up of moss, stone lantern, maple | Each season | 1:1, 4:5 |
| Night exterior | Building lit up at evening | Night | 16:9 |
| Surrounding landscape | Mountains, river, town context | Day | 16:9 |
| Seasonal exterior | Cherry blossoms / snow / foliage with building | Per season | 16:9 |
| Aerial/drone | Bird's-eye view showing setting | Day | 16:9 |

#### Rooms (6-10 images per room type)

| Shot | Description | Notes |
|------|-------------|-------|
| Wide room view | Full room from doorway | Show scale, natural light |
| Room detail -- futon | Bedding laid out for evening | Warm lighting |
| Room detail -- tokonoma | Alcove with scroll and flower arrangement | Cultural detail |
| Window view | View from room window/balcony | Seasonal variant |
| Room amenities | Yukata, tea set, toiletries | Flat-lay or arranged |
| Private bath (if applicable) | In-room cypress bath or onsen | With steam |
| Room at night | Evening atmosphere with lighting | Warm tones |

#### Onsen / Bath (6-8 images)

| Shot | Description | Notes |
|------|-------------|-------|
| Outdoor bath (rotenburo) | Open-air bath with scenery | With steam, no people or tasteful silhouette |
| Indoor bath | Large communal bath | Clean, inviting |
| Private bath | Kashikiri-buro | Intimate setting |
| Bath detail | Water surface, wooden bucket, towels | Close-up texture |
| Seasonal bath | Snow on rocks / autumn leaves floating | Signature shot |
| Changing room | Clean, well-stocked amenities | Shows quality |

#### Dining (8-12 images)

| Shot | Description | Notes |
|------|-------------|-------|
| Full kaiseki spread | Complete multi-course dinner display | Overhead or 45-degree |
| Individual course | Sashimi, grilled dish, seasonal plate | Styled, macro |
| Breakfast spread | Traditional Japanese breakfast | Morning light |
| Seasonal ingredient | Local specialty, fresh catch, vegetables | Story-telling |
| Dining room setting | Private dining room or hall | Show atmosphere |
| Chef at work | Food preparation, knife skills | Artisan focus |
| Sake/drinks | Local sake, tea service | Paired with food |
| Dessert/sweets | Wagashi, matcha service | Detail shot |

#### Facilities & Experience (6-10 images)

| Shot | Description | Notes |
|------|-------------|-------|
| Lobby/reception | Welcoming first impression | With staff if possible |
| Lounge/common area | Reading nook, irori fireplace | Inviting atmosphere |
| Corridor/hallway | Beautiful passages, wooden floors | Architectural beauty |
| Gift shop | Local crafts, souvenirs | If applicable |
| Cultural experience | Tea ceremony, calligraphy, cooking class | Guests participating |
| Welcome tea | Matcha and wagashi on arrival | Omotenashi moment |
| Yukata/kimono | Guests in yukata enjoying the inn | Lifestyle shot |

#### Seasonal (4+ images per season, 16+ total)

| Season | Key Shots |
|--------|-----------|
| **Spring** | Cherry blossoms with building, sakura-themed kaiseki, garden in bloom |
| **Summer** | Lush greenery, fireflies, river/waterfall, refreshing cuisine |
| **Autumn** | Red/gold foliage, maple close-ups, autumn kaiseki, garden at peak color |
| **Winter** | Snow-covered roof, outdoor bath in snow, warm nabe cuisine, kotatsu |

### 6.2 Image Technical Specifications

| Use Case | Resolution | Format | Max File Size |
|----------|-----------|--------|---------------|
| Hero/Full-bleed | 2560x1440px (desktop), 1080x1920px (mobile) | WebP with JPEG fallback | 200-400KB |
| Gallery images | 1920x1280px | WebP with JPEG fallback | 150-300KB |
| Thumbnails | 600x400px | WebP | 30-60KB |
| Room cards | 800x600px | WebP | 50-100KB |
| OG/Social share | 1200x630px | JPEG | 100KB |

### 6.3 Additional Visual Assets

- **Logo:** SVG format, both horizontal and stacked versions, Japanese and English variants
- **Favicon:** ICO + SVG, incorporating mon (家紋) or simplified logo mark
- **Icons:** Custom icon set for amenities (Wi-Fi, parking, onsen, meals, etc.) in SVG
- **Patterns/Textures:** Subtle washi paper texture, wood grain, stone texture for backgrounds
- **Seasonal graphics:** Small illustrations or icons for cherry blossom, maple leaf, snow crystal, etc.
- **Map illustrations:** Custom illustrated map showing access routes (a common feature on Japanese hotel sites)

---

## 7. UX Best Practices

### 7.1 Booking Flow Optimization

The booking experience is the conversion-critical path. Every friction point costs reservations.

**Recommended Flow (4 steps maximum):**

```
Step 1: Select Dates + Guests
  └── Calendar picker + guest count (embedded in header or hero)

Step 2: Choose Plan
  └── Display available plans with room photos, meal info, price
  └── Filter by: price, meal inclusion, room type
  └── Clear comparison between options

Step 3: Enter Guest Information
  └── Auto-fill where possible
  └── Minimal required fields
  └── Remember returning guests

Step 4: Confirm & Pay
  └── Full summary with total cost breakdown
  └── Multiple payment options
  └── Clear cancellation policy
```

**Key principles:**
- Booking widget should be visible on every page (sticky header or floating button)
- Never redirect to a third-party domain for booking
- Show real-time availability -- do not make guests submit a form and wait for response
- Mobile booking must be completable in under 3 minutes
- Progress indicator showing step 1/4, 2/4, etc.
- Save incomplete bookings and offer to resume

### 7.2 Mobile Optimization

72% of travelers prefer to book online, and approximately 60% of travel traffic comes from mobile devices.

**Critical mobile requirements:**

| Aspect | Requirement |
|--------|-------------|
| **Responsive design** | Fluid layouts, not just scaled-down desktop |
| **Touch targets** | Minimum 44x44px for all interactive elements |
| **Sticky booking CTA** | Fixed "Reserve" button at bottom of mobile viewport |
| **Hamburger menu** | Clean, organized with language switcher accessible |
| **Image optimization** | Serve mobile-sized images via `srcset` and `<picture>` |
| **Form design** | Single-column forms, appropriate input types (tel, email, date) |
| **Font size** | Minimum 16px body text to prevent iOS zoom |
| **Swipe gestures** | Gallery and room images support horizontal swipe |
| **Click-to-call** | Phone number is tappable on mobile |
| **Maps integration** | "Open in Maps" link for directions |

### 7.3 Loading Speed & Performance

Hotel websites are image-heavy by nature. Performance optimization is non-negotiable.

**Target metrics (Core Web Vitals):**

| Metric | Target | Description |
|--------|--------|-------------|
| **LCP** (Largest Contentful Paint) | < 2.5 seconds | Hero image must load fast |
| **INP** (Interaction to Next Paint) | < 200ms | Booking widget must respond instantly |
| **CLS** (Cumulative Layout Shift) | < 0.1 | No jumping content as images load |

**Performance strategies:**

| Strategy | Implementation |
|----------|---------------|
| **Modern image formats** | Serve WebP/AVIF with JPEG fallback via `<picture>` element |
| **Lazy loading** | `loading="lazy"` on all below-fold images |
| **Responsive images** | `srcset` with multiple resolutions (400w, 800w, 1600w, 2560w) |
| **CDN** | Serve static assets from CDN nodes close to target audiences (Japan, Asia, US, EU) |
| **Critical CSS** | Inline above-fold CSS, defer remainder |
| **Font subsetting** | For Japanese fonts, subset to JIS Level 1 kanji (~3,000 characters) to reduce 5MB+ font files to ~500KB |
| **Preloading** | `<link rel="preload">` for hero image and primary font |
| **Compression** | Brotli or gzip compression on server |
| **Caching** | Long cache headers for static assets (images, fonts, CSS) |
| **Video optimization** | Use poster images, lazy-load video, consider streaming instead of download |

### 7.4 Navigation & Information Architecture

**Header navigation:**
- Logo (left) -- links to homepage
- Primary navigation (center or right) -- 5-7 items maximum
- Language switcher + Booking CTA (right)
- Transparent header over hero, becomes solid on scroll

**Mobile navigation:**
- Hamburger menu with full-screen overlay
- Booking button always visible outside the menu
- Language switcher at the top of the mobile menu

**Footer:**
- Complete sitemap links
- Contact information, address, phone
- Social media links
- Partner/certification logos (Japan Ryokan Association, etc.)
- Copyright and legal links

### 7.5 Content Strategy for Trust & Conversion

| Element | Purpose | Placement |
|---------|---------|-----------|
| **"How to Spend Your Stay"** | Helps guests imagine the experience | Dedicated page + homepage teaser |
| **Staff/Owner Story** | Builds personal connection | About page |
| **"Getting Here" Guide** | Removes access anxiety | Access page with step-by-step photos |
| **Neighborhood Guide** | Extends value beyond the property | Experience/attractions page |
| **Seasonal Calendar** | Creates urgency and timing guidance | Homepage banner + dedicated page |
| **Price Transparency** | Builds trust, reduces drop-off | All plan listings |
| **Guest Photos** | Social proof with authenticity | Gallery and reviews section |

### 7.6 Accessibility (WCAG 2.1 AA)

| Requirement | Implementation |
|-------------|---------------|
| **Color contrast** | Minimum 4.5:1 ratio for body text, 3:1 for large text |
| **Alt text** | Descriptive alt text on all images, in the page's language |
| **Keyboard navigation** | All interactive elements reachable via tab key |
| **Screen reader support** | ARIA labels on dynamic content, booking widget, gallery |
| **Focus indicators** | Visible focus styles on all interactive elements |
| **Language declarations** | Correct `lang` attribute on `<html>` and mixed-language spans |
| **Form labels** | All form inputs have associated visible labels |
| **Error handling** | Clear, specific error messages for booking forms |

---

## 8. Reference Websites

The following websites exemplify best practices in Japanese hospitality web design:

| Website | Type | Notable Design Elements |
|---------|------|------------------------|
| [HOSHINOYA](https://hoshinoresorts.com/en/brands/hoshinoya/) | Luxury ryokan brand | Full-bleed photography, cinematic scrolling, zen minimalism |
| [Hiiragiya](https://www.hiiragiya.co.jp/en/) | Historic Kyoto ryokan | Cultural storytelling, elegant typography, 200+ year heritage |
| [Selected Ryokan](https://selected-ryokan.com/) | Curated ryokan platform | Clean grid layout, excellent categorization, booking integration |
| [The Ryokan Collection](https://www.ryokancollection.com/) | Luxury ryokan consortium | Editorial photography, brand consistency, multilingual |
| [Not a Hotel](https://notahotel.com/) | Contemporary hospitality | Ultra-minimal, full-bleed images, muted palette, fade-in animations |

---

## 9. Sources

### Design Trends & Web Design
- [Web Design Trends 2025: Insights from Japan's Digital Frontier - Netwise](https://www.netwise.jp/blog/web-design-trends-2025-insights-from-japans-digital-frontier/)
- [Japanese Web Design in 2025: Still Quirky, but More Modernized - iCrossBorder Japan](https://www.icrossborderjapan.com/en/blog/website-design/japanese-web-design-trends/)
- [Best Japanese Web Design of 2026 - MyCodelessWebsite](https://mycodelesswebsite.com/japanese-web-design/)
- [Luxury Hotel Website Design - 52 Inspiring Examples (2025) - Mediaboom](https://mediaboom.com/news/luxury-hotel-website-design/)
- [Hotel Website Design Trends for 2026 That Actually Increase Conversions - DriftTravel](https://drifttravel.com/hotel-website-design-trends-for-2026-that-actually-increase-conversions/)
- [Hotel Website Design Trends for Higher Bookings in 2026 - Mediaboom](https://mediaboom.com/news/hotel-website-design-trends/)
- [Top Web Design Trends for 2026 - Figma](https://www.figma.com/resource-library/web-design-trends/)
- [Japandi Design in 2026: Where Warm Minimalism is Heading - FrescoForma](https://frescoforma.com/japandi-design-2026/)

### Color & Palettes
- [The Color Palette of Wabi-Sabi: Exploring Timeless Color Schemes in 2025 - Astrid Auxier](https://astridauxier.com/wabi-sabi-color-palette/)
- [250 Traditional Colors of Japan - Color Term](https://color-term.com/traditional-color-of-japan/)
- [NIPPON COLORS: Japanese Traditional Color Overview - Art Learnings](https://artlearnings.com/2024/02/14/nippon-colors-overview-of-250-japanese-traditional-colors/)
- [9 Luxury Color Palettes That Define High-End Design in 2025 - Brandlic](https://brandlic.studio/9-luxury-color-palettes-that-define-high-end-design-in-2025/)
- [Luxury Website Colors: Design Tips for Premium Brands - Hook Agency](https://hookagency.com/blog/luxury-website-colors/)
- [Japanese Traditional Colors - ColorFYI Blog](https://colorfyi.com/blog/japanese-traditional-colors/)

### Typography
- [Useful Japanese Web Fonts on Google Fonts - JStockMedia](https://jstockmedia.com/blog/practical-japanese-web-fonts-on-google-fonts/)
- [Noto Serif JP - Google Fonts](https://fonts.google.com/noto/specimen/Noto+Serif+JP)
- [Zen Maru Gothic - Google Fonts](https://fonts.google.com/specimen/Zen+Maru+Gothic)
- [Zen Kaku Gothic New - Google Fonts](https://fonts.google.com/specimen/Zen+Kaku+Gothic+New)
- [Design Yokocho - Top 10 FREE Traditional Mincho Fonts](https://designyokocho.com/notes/traditional-mincho-fonts)
- [Best Google Font Pairings for UI Design in 2025 - Medium](https://medium.com/design-bootcamp/best-google-font-pairings-for-ui-design-in-2025-ba8d006aa03d)

### UX & Booking
- [Mobile Booking Experience for Hotel Websites: A Complete Guide for 2026 - OneWebCare](https://onewebcare.com/blog/mobile-booking-experience-for-hotel-websites/)
- [Booking UX Best Practices to Boost Conversions in 2025 - Ralabs](https://ralabs.org/blog/booking-ux-best-practices/)
- [Travel Site UX: 5 Best Practices - Baymard Institute](https://baymard.com/blog/travel-site-ux-best-practices)
- [How UX/UI Can Improve Hotel Booking Platforms - SennaLabs](https://sennalabs.com/blog/how-ux-ui-can-improve-hotel-booking-platforms)

### Image Optimization
- [How to Optimize Website Images: The Complete 2026 Guide - Request Metrics](https://requestmetrics.com/web-performance/high-performance-images/)
- [Image Optimization 2025: WebP, AVIF & Best Practices Guide - FrontendTools](https://www.frontendtools.tech/blog/modern-image-optimization-techniques-2025)
- [10 Proven Strategies for Hotel Website Speed Optimization - DataFirst Digital](https://datafirstdigital.com/10-proven-strategies-for-hotel-website-speed-optimization/)

### Accessibility
- [Lost in Translation: Tips for Multilingual Web Accessibility - Ben Myers](https://benmyers.dev/blog/multilingual-web-accessibility/)
- [Language Selector Design: 2025 Best Practices for Great UX - Linguise](https://www.linguise.com/blog/guide/best-practices-designing-language-selector/)

### Ryokan & Hospitality Reference
- [Ryokan Stays in Japan 2026 - Refer Japan](https://referjapan.com/ryokan-stays-japan-2026/)
- [Ryokan Guide - Traditional Japanese Inns - Japanko](https://japanko-official.com/ryokan-guide-traditional-japanese-inns/)
- [Japan Ryokan and Hotel Association](https://www.ryokan.or.jp/english/)
- [Japanese Ryokan Guide - Japan National Tourism Organization](https://www.japan.travel/en/guide/japanese-ryokan/)

---

*Report compiled March 2026. All hex codes and font names verified against current availability on Google Fonts and standard web color references.*
