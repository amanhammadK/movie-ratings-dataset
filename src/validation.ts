import { z } from "zod";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_PATH = join(__dirname, "..", "data", "dataset.json");

export const MovieRatingSchema = z.object({
  id: z.string(),
  title: z.string(),
  genre: z.string(),
  rating: z.number().int().min(1).max(5),
  review_text: z.string().optional(),
  user_id: z.string().optional(),
  timestamp: z.string().optional(),
  helpful_votes: z.number().int().min(0).optional(),
  verified_purchase: z.boolean().optional(),
  release_year: z.number().int().optional(),
  director: z.string().optional(),
  runtime_minutes: z.number().int().optional(),
});

export const DatasetSchema = z.array(MovieRatingSchema);
export type MovieRating = z.infer<typeof MovieRatingSchema>;

export function loadAndValidate(): { valid: MovieRating[]; errors: z.ZodError[] } {
  const raw = JSON.parse(readFileSync(DATA_PATH, "utf-8"));
  const valid: MovieRating[] = [];
  const errors: z.ZodError[] = [];
  for (const item of raw) {
    const result = MovieRatingSchema.safeParse(item);
    if (result.success) {
      valid.push(result.data);
    } else {
      errors.push(result.error);
    }
  }
  return { valid, errors };
}

export function validateRecord(record: unknown): record is MovieRating {
  return MovieRatingSchema.safeParse(record).success;
}
