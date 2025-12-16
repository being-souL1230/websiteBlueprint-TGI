let currentCompany = null;

async function openCompanyModal(companyId) {
    try {
        const response = await fetch(`/api/company/${companyId}`);
        const company = await response.json();
        
        if (company.error) {
            alert('Company not found');
            return;
        }
        
        currentCompany = company;
        
        const modalBody = document.getElementById('modalBody');
        modalBody.innerHTML = `
            <div class="company-detail-header">
                <div>
                    <p class="modal-kicker">Featured partner</p>
                    <h2>${company.name}</h2>
                </div>
                <span class="pill pill-salary">${company.salary}</span>
            </div>
            <div class="modal-meta-row">
                <span class="pill pill-req">${company.requirements}</span>
                <span class="pill pill-services">${company.services}</span>
            </div>
            <div class="detail-grid">
                <div class="detail-item">
                    <div class="detail-icon" aria-hidden="true">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                            <path d="M9 8h.01M15 8h.01M9 12h.01M15 12h.01M9 16h.01M15 16h.01"></path>
                            <path d="M8 21v-3h8v3"></path>
                        </svg>
                    </div>
                    <div>
                        <h4>About</h4>
                        <p>${company.about}</p>
                    </div>
                </div>
                <div class="detail-item">
                    <div class="detail-icon" aria-hidden="true">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="12" r="8"></circle>
                            <circle cx="12" cy="12" r="4"></circle>
                            <path d="M12 2v2m0 16v2m10-10h-2M4 12H2m15.5-7.5-1.4 1.4M7.9 16.6l-1.4 1.4m0-12.4 1.4 1.4m8.2 8.2 1.4 1.4"></path>
                        </svg>
                    </div>
                    <div>
                        <h4>Role Requirements</h4>
                        <p>${company.requirements}</p>
                    </div>
                </div>
                <div class="detail-item">
                    <div class="detail-icon" aria-hidden="true">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M20 12v7a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-7z"></path>
                            <path d="M3 9h18v3H3z"></path>
                            <path d="M12 9v12"></path>
                            <path d="M12 9H8.5A2.5 2.5 0 1 1 11 6.5c0 .7-.3 1.3-.7 1.7L12 9z"></path>
                            <path d="M12 9h3.5A2.5 2.5 0 1 0 13 6.5c0 .7.3 1.3.7 1.7L12 9z"></path>
                        </svg>
                    </div>
                    <div>
                        <h4>Benefits & Services</h4>
                        <p>${company.services}</p>
                    </div>
                </div>
            </div>
            <div class="modal-cta-row">
                <button class="btn-apply" onclick="openApplicationModal()">Apply Now</button>
                <p class="modal-note">Tap apply to auto-fill the company name in the form.</p>
            </div>
        `;
        
        document.getElementById('companyModal').style.display = 'block';
        document.body.style.overflow = 'hidden';
    } catch (error) {
        console.error('Error fetching company details:', error);
        alert('Error loading company details. Please try again.');
    }
}

function closeModal() {
    document.getElementById('companyModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

function openApplicationModal() {
    closeModal();
    document.getElementById('applicationForm').reset();
    document.getElementById('applyingFor').textContent = `Applying for: ${currentCompany.name}`;
    document.getElementById('companyApplied').value = currentCompany.name;
    document.getElementById('applicationModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeApplicationModal() {
    document.getElementById('applicationModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

async function submitApplication(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = {
        name: form.name.value,
        age: form.age.value,
        email: form.email.value,
        phone: form.phone.value,
        qualification: form.qualification.value,
        experience: form.experience.value,
        company_applied: form.company_applied.value
    };
    
    try {
        const response = await fetch('/api/apply', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            const modalContent = document.querySelector('.application-modal');
            modalContent.innerHTML = `
                <span class="close" onclick="closeApplicationModal()">&times;</span>
                <div class="success-message">
                    <div class="checkmark">&#10003;</div>
                    <h3>Application Submitted!</h3>
                    <p>Thank you for applying to ${currentCompany.name}. Our team will review your application and contact you soon.</p>
                    <button class="btn-submit" onclick="closeApplicationModal()" style="margin-top: 1.5rem;">Close</button>
                </div>
            `;
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        console.error('Error submitting application:', error);
        alert('Error submitting application. Please try again.');
    }
}

window.onclick = function(event) {
    const companyModal = document.getElementById('companyModal');
    const applicationModal = document.getElementById('applicationModal');
    
    if (event.target === companyModal) {
        closeModal();
    }
    if (event.target === applicationModal) {
        closeApplicationModal();
    }
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
        closeApplicationModal();
    }
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Lightweight client-side search/filter for company cards
const searchInput = document.getElementById('companySearch');
const companyCards = Array.from(document.querySelectorAll('.company-card'));
const emptyState = document.getElementById('companiesEmpty');
const openButtons = Array.from(document.querySelectorAll('.js-open-company'));

function filterCompanies(term) {
    const query = term.trim().toLowerCase();
    let visibleCount = 0;
    companyCards.forEach(card => {
        const name = card.dataset.name || '';
        const meta = card.dataset.meta || '';
        const match = !query || name.includes(query) || meta.includes(query);
        card.style.display = match ? 'flex' : 'none';
        if (match) visibleCount += 1;
    });
    if (emptyState) {
        emptyState.hidden = visibleCount !== 0;
    }
}

if (searchInput) {
    searchInput.addEventListener('input', (e) => filterCompanies(e.target.value));
}

// Attach click handlers for "View details & apply" buttons
openButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const card = btn.closest('.company-card');
        const companyId = card?.dataset.companyId;
        if (companyId) {
            openCompanyModal(companyId);
        }
    });
});
