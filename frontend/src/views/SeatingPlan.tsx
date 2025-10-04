import React, { useEffect, useState } from 'react';
import { Box, Typography, Paper, Card, CardContent } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { studentsApi } from '../api';
import type { Student } from '../api/types';

const SeatingPlan: React.FC = () => {
  const { t } = useTranslation();
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const data = await studentsApi.getAll();
        setStudents(data);
      } catch (error) {
        console.error('Failed to fetch students:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <Typography>{t('app.loading')}</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        {t('nav.seatingPlan')}
      </Typography>

      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="body1" color="text.secondary" gutterBottom>
          Interactive seating plan - Click on a student to record behaviors, absences, etc.
        </Typography>

        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, mt: 2 }}>
          {students.map((student) => (
            <Box key={student.id} sx={{ flex: '0 0 auto', width: { xs: '45%', sm: '30%', md: '23%', lg: '15%' } }}>
              <Card
                sx={{
                  cursor: 'pointer',
                  '&:hover': {
                    boxShadow: 3,
                    transform: 'scale(1.02)',
                    transition: 'all 0.2s',
                  },
                }}
                onClick={() => {
                  // This would open a dialog for recording behaviors
                  console.log('Selected student:', student);
                }}
              >
                <CardContent>
                  <Typography variant="subtitle2" align="center">
                    {student.first_name} {student.last_name}
                  </Typography>
                  <Typography variant="caption" align="center" display="block" color="text.secondary">
                    {student.class_name}
                  </Typography>
                </CardContent>
              </Card>
            </Box>
          ))}
        </Box>

        {students.length === 0 && (
          <Typography color="text.secondary" align="center" sx={{ mt: 4 }}>
            No students found. Import students from CSV in Settings.
          </Typography>
        )}
      </Paper>
    </Box>
  );
};

export default SeatingPlan;
