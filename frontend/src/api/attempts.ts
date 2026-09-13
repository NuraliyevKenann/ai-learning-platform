export type SubmitAttemptInput = {
  exerciseId: string;
  answer: string;
};

export async function submitAttempt(_input: SubmitAttemptInput) {
  throw new Error("submitAttempt is not implemented yet");
}
