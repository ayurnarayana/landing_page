# Ayur Narayana - Doctor-Led Physiotherapy Website

## Overview
This is a complete website redesign for Ayur Narayana, reflecting the evolution from a single-doctor service to a **doctor-led physiotherapy team model**. The website emphasizes expert supervision by Dr. Bhavana while showcasing the scalability and reliability of the certified therapist network.

## Key Features

### 🎯 Doctor-Led Team Positioning
- Highlights Dr. Bhavana's role in evaluating every case
- Emphasizes expert supervision and quality control
- Showcases the professional team network
- Balances trust of specialist care with efficiency of team delivery

### 📱 Responsive Design
- Mobile-first approach
- Elegant, medical-professional aesthetic
- Healing green and gold color palette
- Smooth animations and transitions

### 🔧 Complete Sections
1. **Hero Section** - Expert-supervised care messaging
2. **Trust Section** - The Ayur Narayana difference
3. **How It Works** - 4-step process (Request → Evaluation → Treatment → Supervision)
4. **Services** - 6 comprehensive service categories with images
5. **About Dr. Bhavana** - Medical leadership and expertise
6. **Our Team** - Certified professionals overview
7. **Why Choose Us** - Benefits of expert-led team care
8. **Testimonials** - Patient success stories
9. **Coverage** - Bangalore service areas
10. **Contact Form** - Request assessment

## File Structure

```
├── index.html                 # Main website file
├── IMAGE_GUIDE.md            # Complete image specifications guide
├── static/
│   ├── css/
│   │   └── style.css         # Comprehensive styles
│   ├── js/
│   │   └── script.js         # Interactive functionality
│   └── images/               # Image placeholder directory
│       └── (Add your images here)
```

## Image Placeholders

### Required Images (22 total):

**Brand Assets:**
- `logo.png` - Company logo

**Hero Section:**
- `hero-bg.jpg` - Background image
- `hero-main.jpg` - Main hero image

**Process Icons:**
- `step-1.png` through `step-4.png` - Process step icons

**Services (6 images):**
- `service-orthopedic.jpg`
- `service-neurological.jpg`
- `service-geriatric.jpg`
- `service-cardio.jpg`
- `service-womens.jpg`
- `service-pediatric.jpg`

**Team & About:**
- `dr-bhavana.jpg` - Professional portrait
- `team-photo.jpg` - Team group photo

**Testimonials:**
- `patient-1.jpg`, `patient-2.jpg`, `patient-3.jpg`

**Coverage:**
- `bangalore-map.png` - Service area map

📋 **See IMAGE_GUIDE.md for detailed specifications, sizes, and recommendations for each image**

## Setup Instructions

### 1. Add Your Images
Place all images in `static/images/` directory following the specifications in IMAGE_GUIDE.md

### 2. Customize Content
Edit `index.html` to update:
- Contact information (phone, email)
- Statistics (patients treated, therapist count)
- Service area localities
- Testimonial details
- Any specific business information

### 3. Deploy
Upload all files to your web hosting:
- Maintain the directory structure
- Ensure `static/` folder is at the same level as `index.html`
- Test on multiple devices

## Design Philosophy

### Color Palette
- **Primary Green** (#2D5F4D) - Trust, healing, professionalism
- **Accent Gold** (#D4A574) - Premium quality, warmth
- **Cream/Neutral** (#FAF8F5) - Clean, calming, medical

### Typography
- **Headings:** Cormorant Garamond (elegant, professional serif)
- **Body:** Nunito Sans (modern, readable sans-serif)

### Key Messaging
✅ Expert supervision by Dr. Bhavana
✅ Certified professional team
✅ Fast response (24 hours)
✅ Home comfort and convenience
✅ Consistent quality through standardized protocols
✅ Continuous progress monitoring

## Browser Compatibility
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Features Implemented

### Interactive Elements
- Smooth scroll navigation
- Form validation and submission
- Animated statistics counter
- Scroll-triggered animations
- Mobile responsive menu
- Hover effects on cards

### Performance
- Optimized CSS
- Lazy loading ready
- Compressed file structure
- Fast load times

## Customization Tips

### Change Colors
Edit CSS variables in `static/css/style.css`:
```css
:root {
    --primary-green: #2D5F4D;
    --accent-gold: #D4A574;
    /* etc. */
}
```

### Update Contact Info
Find and replace in `index.html`:
- Email: `contact@ayurnarayana.com`
- Phone: `+91 98765 43210`

### Add/Remove Services
Edit the services grid section in `index.html` - each service is a self-contained `.service-card` div

## Next Steps

1. ✅ Review IMAGE_GUIDE.md for image requirements
2. ✅ Gather and prepare all images
3. ✅ Place images in `static/images/` directory
4. ✅ Customize business-specific content
5. ✅ Test locally in a browser
6. ✅ Deploy to web hosting
7. ✅ Test on mobile devices
8. ✅ Set up form backend (currently alerts only)

## Support & Maintenance

### Form Integration
The contact form currently shows an alert. To integrate with a backend:
1. Add form action endpoint
2. Update JavaScript in `static/js/script.js`
3. Set up email notifications or CRM integration

### Analytics
Add Google Analytics or similar by inserting tracking code before `</head>` tag

## Notes

- All HTML comments indicate image placeholders
- Placeholder backgrounds show gray if images are missing
- Layout remains professional even without images
- Fully accessible with semantic HTML
- SEO-friendly structure

---

**Ayur Narayana - Expert-Supervised Physiotherapy at Your Doorstep**

For questions or support, refer to the documentation files included.
