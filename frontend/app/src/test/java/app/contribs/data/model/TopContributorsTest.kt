package app.contribs.data.model

import com.google.gson.Gson
import org.junit.Assert.assertEquals
import org.junit.Test

class TopContributorsTest {
    @Test
    fun testJsonParsing() {
        val json = """
            {
                "top_individuals": [
                    {
                        "name": "John Doe",
                        "total": 1000.0,
                        "employer_name": "Acme Corp"
                    }
                ],
                "top_employers": [
                    {
                        "name": "Acme Corp",
                        "total": 5000.0
                    }
                ]
            }
        """.trimIndent()

        val gson = Gson()
        val response = gson.fromJson(json, TopContributorsResponse::class.java)

        assertEquals(1, response.topIndividuals.size)
        assertEquals("John Doe", response.topIndividuals[0].name)
        assertEquals(1000.0, response.topIndividuals[0].total, 0.0)
        assertEquals("Acme Corp", response.topIndividuals[0].employerName)

        assertEquals(1, response.topEmployers.size)
        assertEquals("Acme Corp", response.topEmployers[0].name)
        assertEquals(5000.0, response.topEmployers[0].total, 0.0)
    }
}
