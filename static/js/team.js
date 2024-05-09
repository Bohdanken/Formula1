 /*
AJAX
    */
    $(document).ready(function() {
        // Attach a click event listener to each tab
        $('.tab').click(function() {
              $('.tab').removeClass('active');
                $(this).addClass('active');
            const username = $(this).data('username');
            const teamSlug = $(this).data('team');
            console.log("Making AJAX call for:", username);
            $.ajax({
                type: 'GET', // Method type GET since we are fetching data
                url: `/formula/team/${teamSlug}/?profile=${username}`, // Adjust URL as needed
                success: function(response) {
                $('#pfp').attr('src', response.picture_url);
                $('.member_information h2:first').text(`${response.role} · ${response.username}`);
                $('.member_information h2:eq(1)').text(`Full name: ${response.full_name}`);
                $('.member_information span:eq(0)').text(`Member since: ${response.member_since}`);
                $('.member_information span:eq(1)').text(`Last login: ${response.last_login}`);
                $('.member_information span:eq(2)').text(`Student Id: ${response.student_id}`);
                $('.member_information span:eq(3)').text(`Email: ${response.email}`);
                if(response.bio && response.bio.trim() !== "") {
                    $('.member_information span:eq(4)').html(`Bio: ${response.bio}`);
                } else {
                    $('.member_information span:eq(4)').html('<i>User has no bio set</i>');
                }
            },
                error: function(error) {
                    console.error('Error loading the profile:', error);
                }
            });
        });
    });


