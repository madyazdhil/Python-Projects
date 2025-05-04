


$(document).ready(function() {

    $('#submitBtn').click(function() {
        const answer = $('#answer').val().trim();
        if (!answer) {
            showAlert('Error', 'Please enter your answer before submitting.', 'danger');
            return;
        }

        // Disable the button to prevent multiple submissions
        $(this).prop('disabled', true);

        // Use the full jQuery AJAX method
        $.ajax({
            url: '/check_answer',
            type: 'POST',
            data: $('#quizForm').serialize(),
            success: function(response) {
                if (response.status === 'correct') {
                    showAlert('Success', response.message, 'success');
                    updateButtonForCorrectAnswer();
                } else {
                    showAlert('Incorrect', response.message, 'danger');
                }
            },
            error: function() {
                showAlert('Error', 'An error occurred while checking your answer.', 'danger');
            },
            complete: function() {
                // Re-enable the button
                $('#submitBtn').prop('disabled', false);
            }
        });
    });

    function showAlert(title, message, type = 'info') {
        // Remove any existing alerts
        $('.alert').alert('close');

        // Create the alert HTML
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                <strong>${title}</strong> ${message}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        `;

        // Append to container and show
        $('#alertContainer').append(alertHtml);

        // Auto-close after 5 seconds
        setTimeout(() => {
            $('.alert').alert('close');
        }, 5000);
    }

    function updateButtonForCorrectAnswer() {
        const $btn = $('#submitBtn');
        $btn.removeClass('btn-primary btn-success btn-warning');

        // Check if this is the last question
        const progressPercentage = parseInt($('.progress-bar').css('width')) / parseInt($('.progress-bar').parent().css('width'));
        const totalQuestions = quizData.totalQuestions;
        const answeredQuestions = quizData.answeredQuestions + 1; // +1 because we just answered correctly

        if (answeredQuestions >= totalQuestions) {
            // Last question - change to "Go Back"
            $btn.addClass('btn-warning')
                .text('Go Back')
                .off('click')
                .click(function() {
                    window.location.href = '/';
                });
        } else {
            // Not last question - change to "Next Question"
            $btn.addClass('btn-success')
                .text('Next Question')
                .off('click')
                .click(function() {
                    window.location.href = '/next_question';
                });
        }
    }
});