// solve the issue can not receive confirmation email from AWS Cognito
export const handler = async(event) => {
    event.response.autoConfirmUser = true;
    event.response.autoVerifyEmail = true; // Optional: Set to true if you want to auto-verify the email
    event.response.autoVerifyPhone = false; // Optional: Set to true if you want to auto-verify the phone number
    return event;
};
