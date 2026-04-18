// form-handler.js
// Form submission handler for patient requests

/**
 * Submit patient request to Supabase database
 * @param {Object} formData - The form data to submit
 * @returns {Promise<Object>} - Response from database
 */
async function submitPatientRequest(formData) {
    try {
        const requestData = {
            patient_name: formData.name,
            phone: formData.phone,
            email: formData.email || null,
            location: formData.area,                  // Bangalore area from dropdown
            service_type: formData.service_type,      // NEW: selected service
            condition: formData.condition,
            preferred_time: formData.timing,
            status: 'pending',
            notes: null
        };

        const { data, error } = await window.supabaseClient
            .from('requests')
            .insert([requestData])
            .select();

        if (error) throw error;

        console.log('Request submitted successfully:', data);
        return {
            success: true,
            data: data[0],
            message: 'Your request has been submitted successfully!'
        };

    } catch (error) {
        console.error('Error submitting request:', error);
        return {
            success: false,
            error: error.message,
            message: 'There was an error submitting your request. Please try again.'
        };
    }
}

/**
 * Create notification for admin about new request
 */
async function notifyAdminNewRequest(patientName, requestId) {
    try {
        const { data: admins, error: adminError } = await window.supabaseClient
            .from('users')
            .select('id')
            .eq('role', 'admin');

        if (adminError) { console.error('Error fetching admins:', adminError); return; }

        const notifications = admins.map(admin => ({
            user_id: admin.id,
            title: 'New Patient Request',
            message: `New request from ${patientName}`,
            is_read: false
        }));

        const { error: notifError } = await window.supabaseClient
            .from('notifications')
            .insert(notifications);

        if (notifError) {
            console.error('Error creating notifications:', notifError);
        } else {
            console.log('Admin notifications created successfully');
        }
    } catch (error) {
        console.error('Error in notifyAdminNewRequest:', error);
    }
}

/**
 * Validate form data before submission
 */
function validateFormData(formData) {
    const errors = [];

    if (!formData.name || formData.name.trim().length < 2) {
        errors.push('Please enter a valid name (minimum 2 characters)');
    }

    if (!formData.phone || !/^[6-9]\d{9}$/.test(formData.phone.replace(/\s+/g, ''))) {
        errors.push('Please enter a valid 10-digit Indian mobile number');
    }

    if (formData.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
        errors.push('Please enter a valid email address');
    }

    // NEW: validate service type
    if (!formData.service_type) {
        errors.push('Please select the service you require');
    }

    // NEW: validate Bangalore area
    if (!formData.area) {
        errors.push('Please select your area in Bangalore');
    }

    if (!formData.condition || formData.condition.trim().length < 10) {
        errors.push('Please describe your condition (minimum 10 characters)');
    }

    if (!formData.timing) {
        errors.push('Please select your preferred timing');
    }

    return {
        isValid: errors.length === 0,
        errors: errors
    };
}

/**
 * Show loading state on submit button
 */
function setButtonLoadingState(button, isLoading) {
    if (isLoading) {
        button.disabled = true;
        button.dataset.originalText = button.textContent;
        button.innerHTML = '<span class="spinner"></span> Submitting...';
        button.style.opacity = '0.7';
    } else {
        button.disabled = false;
        button.textContent = button.dataset.originalText || 'Submit Request';
        button.style.opacity = '1';
    }
}

/**
 * Show success/error message to user
 */
function showMessage(message, type = 'success') {
    const existingMessage = document.querySelector('.form-message');
    if (existingMessage) existingMessage.remove();

    const messageDiv = document.createElement('div');
    messageDiv.className = `form-message form-message-${type}`;
    messageDiv.textContent = message;

    const form = document.getElementById('assessmentForm');
    form.parentNode.insertBefore(messageDiv, form);

    messageDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });

    setTimeout(() => {
        messageDiv.style.opacity = '0';
        setTimeout(() => messageDiv.remove(), 300);
    }, 5000);
}

/**
 * Handle form submission — single handler, no duplicates
 */
async function handleFormSubmit(event) {
    event.preventDefault();

    const formData = {
        name:         document.getElementById('name').value.trim(),
        phone:        document.getElementById('phone').value.trim(),
        email:        document.getElementById('email').value.trim(),
        service_type: document.getElementById('service_type').value,   // NEW
        area:         document.getElementById('area').value,            // NEW
        condition:    document.getElementById('condition').value.trim(),
        timing:       document.getElementById('timing').value
    };

    const validation = validateFormData(formData);

    if (!validation.isValid) {
        showMessage(validation.errors.join(' • '), 'error');
        return;
    }

    const submitButton = event.target.querySelector('button[type="submit"]');

    try {
        setButtonLoadingState(submitButton, true);

        const result = await submitPatientRequest(formData);

        if (result.success) {
            await notifyAdminNewRequest(formData.name, result.data.id);

            showMessage(
                '✅ Thank you! Our team will contact you within 24 hours to confirm your appointment.',
                'success'
            );

            event.target.reset();

            if (window.gtag) {
                gtag('event', 'form_submission', {
                    event_category: 'engagement',
                    event_label: 'patient_request'
                });
            }
        } else {
            throw new Error(result.message);
        }

    } catch (error) {
        console.error('Form submission error:', error);
        showMessage(
            'We encountered an error submitting your request. Please try again or call us at +91 98765 43210.',
            'error'
        );
    } finally {
        setButtonLoadingState(submitButton, false);
    }
}

// Initialize — single event listener
document.addEventListener('DOMContentLoaded', function () {
    const assessmentForm = document.getElementById('assessmentForm');

    if (assessmentForm) {
        assessmentForm.addEventListener('submit', handleFormSubmit);
        console.log('Form handler initialized');
    } else {
        console.error('Assessment form not found');
    }
});

// Export for potential external use
window.submitPatientRequest = submitPatientRequest;
window.validateFormData = validateFormData;